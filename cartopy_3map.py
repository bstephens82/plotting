


import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from cartopy.util import add_cyclic_point

d1=Dataset('/glade/scratch/stepheba/archive/dflt/atm/hist/dflt.cam.h0.1979-01.nc')
d2=Dataset('/glade/scratch/stepheba/archive/dflt/atm/hist/dflt.cam.h0.1979-02.nc')
variable='SWCF'
units='W/m$^2$'

lon=np.array(d1.variables['lon'])
lat=np.array(d1.variables['lat'])
dfltvar0=np.array(d1.variables[variable])

testvar0=np.array(d2.variables[variable])

#rearrange longitude so pacific is centered
dfltvar=np.mean(dfltvar0[:,:,:],0)
testvar=np.mean(testvar0[:,:,:],0)

dfltvarshft=np.zeros((192,288))
testvarshft=np.zeros((192,288))
for i in range(0,288):
    if i<144:
        dfltvarshft[:,i]=dfltvar[:,i+144]
        testvarshft[:,i]=testvar[:,i+144]
    else:
        dfltvarshft[:,i]=dfltvar[:,i-144]
        testvarshft[:,i]=testvar[:,i-144]

lon=lon-180

dfltvarshft2, lon2 = add_cyclic_point(dfltvarshft, coord=lon)
testvarshft2, lon2 = add_cyclic_point(testvarshft, coord=lon)


#create plot
fig, axs = plt.subplots(3,1,subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})

axs=axs.flatten()
mycmap='coolwarm'
cs=axs[0].contourf(lon2,lat,testvarshft2[:,:],transform = ccrs.PlateCarree(),cmap=mycmap,extend='both')
axs[0].set_title('test')
axs[0].coastlines()
cbar=fig.colorbar(cs,ax=axs[0])
cbar.set_label(units)
cs=axs[1].contourf(lon2,lat,dfltvarshft2[:,:],transform = ccrs.PlateCarree(),cmap=mycmap,extend='both')
axs[1].set_title('dflt')
axs[1].coastlines()
cbar=fig.colorbar(cs,ax=axs[1])
cbar.set_label(units)
cs=axs[2].contourf(lon2,lat,testvarshft2[:,:]-dfltvarshft2[:,:],transform = ccrs.PlateCarree(),cmap=mycmap,extend='both')
axs[2].set_title(r'test $-$ dflt')
axs[2].coastlines()
cbar=fig.colorbar(cs,ax=axs[2])
cbar.set_label(units)

plt.savefig('/glade/u/home/stepheba/figs/'+variable+'.png',dpi=300,bbox_inches='tight')
plt.show()


#plt.plot(dfltvar0[:,90,144])
#plt.plot(testvar0[:,90,144])
#plt.show()

