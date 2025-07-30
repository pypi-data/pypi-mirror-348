
def get_contract_time_of_next_n_month(year, month, n):
    month += n
    while month > 12:
        month -= 12
        year += 1
    return str(year % 100) + "%02d" % month


def get_future_symbol_root(spot):
    if spot == "sh000300":
        return "IF"
    if spot == "sh000905":
        return "IC"
    if spot == "sh000852":
        return "IM"
    if spot == "sh000016":
        return "IH"
    return None
