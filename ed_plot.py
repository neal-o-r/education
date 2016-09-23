import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def map_counties(df):

        counties = gpd.GeoDataFrame.from_file('data/counties.shp')

        counties = counties.set_index('NAME_TAG')
        counties = pd.concat([counties, df_tot], axis=1, 
                                 join_axes=[counties.index])

        counties = gpd.GeoDataFrame(counties[counties.PC.notnull()])


        vmin, vmax = counties.PC.min(), counties.PC.max()

        ax = counties.plot(column='PC', scheme='equal_interval', 
                                k=5, colormap='OrRd', alpha=0.5)

        plt.title(r'Percentage of population reporting PhD level education in Census 2011')
        fig = ax.get_figure()
        cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
        sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        
        ax.xaxis.set_visible(False)        
        ax.yaxis.set_visible(False)        

        sm._A = []
        fig.colorbar(sm, cax=cax)

        plt.show()


if __name__ == '__main__':

        df_ed  = pd.read_csv('data/phd_education.csv', skiprows=9)
        df_pop = pd.read_csv('data/pop.csv')
        
        df_ed  = df_ed.set_index('County')
        df_pop = df_pop.set_index('CountyName')
        
        df_tot = pd.concat([df_pop, df_ed], axis=1, join_axes=[df_pop.index])
        df_tot['PC'] = 100*(df_tot.Number / df_tot.Population)
        
        map_counties(df_tot)
