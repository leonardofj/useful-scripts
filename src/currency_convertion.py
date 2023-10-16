from pandasdmx import Request
from datetime import datetime, timedelta
from currency_converter import CurrencyConverter


currency_dict = {
    "$": "USD",
    "USD": "USD",
    "DOLLAR": "USD",
    "€": "EUR",
    "EURO": "EUR",
    "EUROS": "EUR",
    "EUR": "EUR",
    "CA$": "CAD",
    "US$": "USD",
    "£": "GBP",
    "AED": "AED",
    "CN¥": "CNY",
    "RMB": "CNY",
    "A$": "AUD",
    "AU$": "AUD",
    "HK$": "HKD",
    "MX$": "MXN",
    "NZ$": "NZD",
    "R$": "BRL",
    "₹": "INR",
    "RUPEE": "INR",
    "¥": "JPY",
    "YEN": "JPY",
    "₩": "KRW",
    "₪": "ILS",
    "\xe2\x82\xac": "EUR",
    "ILS": "ILS",
    "ISK": "ISK",
    "GBP": "GBP",
    "CAD": "CAD",
    "JPY": "JPY",
    "IDR": "IDR",
    "BGN": "BGN",
    "DKK": "DKK",
    "HUF": "HUF",
    "RON": "RON",
    "MYR": "MYR",
    "SEK": "SEK",
    "SGD": "SGD",
    "HKD": "HKD",
    "AUD": "AUD",
    "CHF": "CHF",
    "KRW": "KRW",
    "CNY": "CNY",
    "TRY": "TRY",
    "HRK": "HRK",
    "NZD": "NZD",
    "THB": "THB",
    "NOK": "NOK",
    "RUB": "RUB",
    "RWF": "RWF",
    "RWANDAN FRANC": "RWF",
    "INR": "INR",
    "MXN": "MXN",
    "CZK": "CZK",
    "BRL": "BRL",
    "PLN": "PLN",
    "PHP": "PHP",
    "ZAR": "ZAR",
    "ZAC": "ZAC",
    "ARS": "ARS",
    "QAR": "QAR",
    "TWD": "TWD",
    "ILA": "ILA",
    "CLP": "CLP",
    "KWF": "KWF",
}


def currency_convertion(
    amount: str | int | float,
    original_currency: str,
    convert_to_currency: str = "EUR",
    date: datetime | None = None,
) -> float:
    """
    Currency convertion for specific date.
    :param amount:
    :param original_currency:
    :param convert_to_currency:
    :param date:
    :return: the converted currency according to the date
    """
    converter = CurrencyConverter(
        fallback_on_missing_rate=True, fallback_on_wrong_date="linear_interpolation"
    )
    amount_euro = converter.convert(
        amount, original_currency, convert_to_currency, date=date
    )
    return round(amount_euro, 2)


def convert_to_euro(
    amount: str | float | int, original_currency: str, date: datetime = datetime.today()
) -> float:
    """
    Convertion to Euro.
    :param amount:
    :param original_currency:
    :param date:
    :return: amount converted to Euro according to the date
    """
    amount_euro = None
    # The Euro foreign exchange reference dates of the ecb are updated around 16:00 CET in every working day.
    # That's why we need to convert the date to an earlier one, if it's the current day, Monday, Sunday, or Saturday
    if date.date() == datetime.now().date() or date.weekday() == 5:
        date = date - timedelta(days=1)
    if date.weekday() == 6:
        date = date - timedelta(days=2)
    if date.weekday() == 0:
        date = date - timedelta(days=3)
    try:
        string_date = date.strftime("%Y-%m-%d")
        ecb = Request("ECB")
        data_response = ecb.data(
            resource_id="EXR",
            key={"CURRENCY": [original_currency]},
            params={"startPeriod": string_date, "endPeriod": string_date},
        )
        data_response = data_response.data

        eur_rate = data_response[0].obs[0].value
        if isinstance(eur_rate, str):
            print("Returned NaN. Retrying currency conversion with fallback option")
            amount_euro = currency_convertion(date, amount, original_currency)
        else:
            origin_cur_rate = 1 / float(eur_rate)
            amount_euro = round(float(amount) * float(origin_cur_rate), 2)

    except Exception:
        print("Retrying currency conversion with fallback option")
        amount_euro = currency_convertion(date, amount, original_currency)

    return amount_euro
