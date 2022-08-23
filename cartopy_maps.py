


import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from cartopy.util import add_cyclic_point

d=Dataset('/glade/scratch/stepheba/archive/dflt/atm/hist/dflt.cam.h0.1979-01.nc')
variable='SWCF'
units='W/m$^2$'

lon=np.array(d.variables['lon'])
lat=np.array(d.variables['lat'])
var0=np.array(d.variables[variable])


#rearrange longitude so pacific is centered
var=np.mean(var0[:,:,:],0)

varshft=np.zeros((192,288))
for i in range(0,288):
    if i<144:
        varshft[:,i]=var[:,i+144]
    else:
        varshft[:,i]=var[:,i-144]

lon=lon-180

varshft2, lon2 = add_cyclic_point(varshft, coord=lon)

#create plot
fig, axs = plt.subplots(1,1,subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})

mycmap='coolwarm'
cs=axs.contourf(lon2,lat,varshft2[:,:],transform = ccrs.PlateCarree(),cmap=mycmap,extend='both')
axs.set_title('test')
axs.coastlines()
cbar=fig.colorbar(cs,ax=axs)
cbar.set_label(units)

#plt.savefig('/glade/u/home/stepheba/figs/'+variable+'.png',dpi=300,bbox_inches='tight')
plt.show()


