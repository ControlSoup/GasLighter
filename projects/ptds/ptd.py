from gaslighter import *
from CoolProp.CoolProp import PropsSI

pressure_psia = np.linspace(14.7, 2000)
temp_degF = np.linspace(0, 250)

def ptd(pressure_psia, temp_degF):
    pressure = convert(pressure_psia, 'psia', 'Pa')
    temp = convert(temp_degF, 'degF', 'degK')
    return convert(
        PropsSI('D', 'P', pressure, 'T', temp, 'N2O'),
        'kg/m^3',
        'lbm/in^3'
    )


graph_countour(
    'Presure [psia]', pressure_psia,
    'Temperature [degF]', temp_degF,
    'Density [lbm/in^3]', ptd,
    title='Pressure vs Temp vs Density [Nitrious Oxide]',
    show_fig=True,
    export_path='plots/n2o_ptd.html'
)