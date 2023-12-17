import locale

locale.setlocale(locale.LC_ALL, locale.getlocale())


def funny(dta):
    if dta[0] == 'fv':
        PV, r, n = [float(x) for x in dta[1:]]
        return PV * (1 + r / 100) ** n
    else:
        FV, r, n = [float(x) for x in dta[1:]]
        return FV / (1 + r / 100) ** n


# pv 4796729.09 7 10
# fv 4796729.09 7 10
# print(PV)
while True:
    print("₹", locale.format_string("%d", funny(input().split()), grouping=True))







