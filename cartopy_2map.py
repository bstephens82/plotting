import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from cartopy.util import add_cyclic_point

d=Dataset('/glade/scratch/stepheba/archive/dflt/atm/hist/dflt.cam.h0.1979-01.nc')
variable1='SWCF'
variable2='TS'
units1='W/m$^2$'
units2='K'

lon=np.array(d.variables['lon'])
lat=np.array(d.variables['lat'])
var10=np.array(d.variables[variable1])
var20=np.array(d.variables[variable2])


#rearrange longitude so pacific is centered
var1=np.mean(var10[:,:,:],0)
var2=np.mean(var20[:,:,:],0)

varshft1=np.zeros((192,288))
varshft2=np.zeros((192,288))
for i in range(0,288):
    if i<144:
        varshft1[:,i]=var1[:,i+144]
        varshft2[:,i]=var2[:,i+144]
    else:
        varshft1[:,i]=var1[:,i-144]
        varshft2[:,i]=var2[:,i-144]

lon=lon-180

#print(lon.shape)
#print(dfltvarshft.shape)

varshft12, lon2 = add_cyclic_point(varshft1, coord=lon)
varshft22, lon2 = add_cyclic_point(varshft2, coord=lon)

#create plot
fig, axs = plt.subplots(2,1,subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})

axs=axs.flatten()
mycmap='coolwarm'
cs=axs[0].contourf(lon2,lat,varshft12[:,:],transform = ccrs.PlateCarree(),cmap=mycmap,extend='both')
axs[0].set_title(variable1)
axs[0].coastlines()
cbar=fig.colorbar(cs,ax=axs[0])
cbar.set_label(units1)
cs=axs[1].contourf(lon2,lat,varshft22[:,:],transform = ccrs.PlateCarree(),cmap=mycmap,extend='both')
axs[1].set_title(variable2)
axs[1].coastlines()
cbar=fig.colorbar(cs,ax=axs[1])
cbar.set_label(units2)

#plt.savefig('/glade/u/home/stepheba/figs/'+variable+'.png',dpi=300,bbox_inches='tight')
plt.show()


