# -*- coding: utf-8 -*-



import pandas, numpy, math, multiprocessing, os
from scipy.stats import chisquare
from scipy.spatial import distance
from functools import partial

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, FormatStrFormatter


def find_average_rho(dots, dot, dc, smal):
    half_of_dc = dc/2
    lage = smal * 2.5
    edge_x_min = min(dots.start1)
    edge_x_max = max(dots.start1)        #for the dots beside the edge of the maps
    edge_y_min = min(dots.start2)        #for the dots beside the edge of the maps
    edge_y_max = max(dots.start2)
    small_square = len(dots.query('@dot[1]-@smal<start1<@dot[1]+@smal and @dot[2]-@smal<start2<@dot[2]+@smal'))
    large_square = len(dots.query('@dot[1]-@lage<start1<@dot[1]+@lage and @dot[2]-@lage<start2<@dot[2]+@lage'))-small_square
    area_sm = (min(dot[1]+smal, edge_x_max) - max(dot[1]-smal, edge_x_min)) * (min(dot[2]+smal, edge_y_max) - max(dot[2]-smal, edge_y_min))
    area_la = (min(dot[1]+lage, edge_x_max) - max(dot[1]-lage, edge_x_min)) * (min(dot[2]+lage, edge_y_max) - max(dot[2]-lage, edge_y_min)) - area_sm
    large_density = large_square/area_la
    average_rho = large_density*(half_of_dc**2)
    return average_rho



def plot_one_spot(dot, bunchDots, saved_dir, window_size = 1000000, smal = 120000):
    point_x=dot[1]
    point_y=dot[2]
    a = bunchDots.dots.query('@point_x - @window_size < start1 < @point_x + @window_size and @point_y - @window_size < start2 < @point_y + @window_size')
    
    #calculate_boundary_rho
    average_rho = find_average_rho(dots = bunchDots.dots, dot = dot, dc = bunchDots.dc, smal = smal)
    boundary_rho = int((a.query('start1==@point_x and start2==@point_y ').rho+average_rho)/2)
    print('boundary Rho:', boundary_rho)
    dots_with_high_rho = a.query('rho > @boundary_rho')
    
    fig,ax=plt.subplots(figsize=[10,10])
    plt.scatter(a['start1'], a['start2'], c='royalblue', s=2)
    plt.scatter(dots_with_high_rho['start1'], dots_with_high_rho['start2'], c='red', s=1.9)
    #   plt.axis([point_x-k2*1.1,point_x+k2*1.1,point_y-k2*1.1,point_y+k2*1.1])
    plt.axvline(point_x+smal, linewidth=1, color='grey', linestyle=':')
    plt.axvline(point_x-smal, linewidth=1, color='grey', linestyle=':')
    plt.axhline(point_y+smal, linewidth=1, color='grey', linestyle=':')
    plt.axhline(point_y-smal, linewidth=1, color='grey', linestyle=':')
    plt.xlabel(str(int(dot[8]-dot[10]/2))+':'+str(int(dot[8]+dot[10]/2)), {'fontsize':15, 'weight':'bold'})
    plt.ylabel(str(int(dot[9]-dot[11]/2))+':'+str(int(dot[9]+dot[11]/2)), {'fontsize':15, 'weight':'bold'})
    #plt.title(clustername, {'fontsize':15, 'weight':'bold'})
    plt.tick_params(labelsize=11)
    formatter0 = EngFormatter(unit='B')
    ax.xaxis.set_major_formatter(formatter0)
    ax.yaxis.set_major_formatter(formatter0)
    plt.axis(option='equal')
    if not os.path.exists(saved_dir):
        os.makedirs(saved_dir)
    plt.savefig(saved_dir + '/bin1_' + str(int(dot[1])) + '_bin2_' + str(int(dot[2])) + '.pdf')
    #plt.show()



