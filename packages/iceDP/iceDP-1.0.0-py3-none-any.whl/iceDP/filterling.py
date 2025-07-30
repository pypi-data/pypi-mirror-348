# -*- coding: utf-8 -*-

# __init__.py
import pandas, numpy, math, multiprocessing
from scipy.stats import chisquare
from scipy.spatial import distance
from functools import partial

def chi_square_test(dot, dc, dots):
    #define a function to find p-value
    dc = dc/6
    xinde = dot[1]
    yinde = dot[2]
    obs = []
    if_zero = []
    for i in (-2*dc, 0, 2*dc):
        xind = xinde + i
        for ii in (-2*dc, 0, 2*dc):
            yind=yinde+ii
            little_counts=sum(dots.query('@xind-@dc <= start1 < @xind+@dc and @yind-@dc <= start2 < @yind+@dc').counts)
            if little_counts == 0:
                if_zero.append(0)
            else:
                if_zero.append(1)
            obs.append(little_counts)
    real_rho=sum(obs)
    exp=numpy.ones(9)*(real_rho/9)
    _,p1=chisquare(obs,exp)
    exp=numpy.array([1, 1, 1, 1, 2, 1, 1, 1, 1])*(real_rho/10)
    _,p2=chisquare(obs, exp)
    p=max(p1,p2)
    return p,sum(if_zero)


def find_average_rho(dots_within_square, dc):
    half_side_length_of_small_square = dc/6
    edge_x_min = min(dots_within_square.start1)
    edge_x_max = max(dots_within_square.start1)        #for the dots beside the edge of the maps
    edge_y_min = min(dots_within_square.start2)        #for the dots beside the edge of the maps
    edge_y_max = max(dots_within_square.start2)
    area_dots = (edge_x_max-edge_x_min)*(edge_y_max-edge_y_min)
    density = len(dots_within_square)/area_dots
    #average_rho = count of dots_within_square / area of dots_within_square * area_dc
    average_rho=density*((half_side_length_of_small_square*3)**2)
    return average_rho


def auto_border(dot, dots, rangess, use_multiply_in_find_rho, dc, x, y, x_sorted, y_sorted):
    '''find the border of the interaction spot.
    main idea:
    calculate a boundary_rho, then, the dots whose rho are larger than the boundary_rho are classified as a whole peak.'''
    point_x=dot[1]
    point_y=dot[2]
    dots_within_square = dots.query('@point_x-@rangess<start1<@point_x+@rangess and @point_y-@rangess<start2<@point_y+@rangess')

    #if use multiply in find rho, then we should re-calculate the rho
    if use_multiply_in_find_rho == True:
        #calculate_rho
        tartget_dots=dots_within_square
        rho = [find_rho(point=i, dc=dc, x=x, y=y, x_sorted=x_sorted, y_sorted=y_sorted,
                            dots=self.dots, use_multiply_in_find_rho = False) for i in tartget_dots.values]
        dots_within_square = dots_within_square.assign(rho=rho)
        
        #calculate_boundary_rho
        average_rho=find_average_rho(dots_within_square, dc)
        rho_max = dots_within_square.query('start1 == @point_x and start2 == @point_y').rho.iloc[0]
        boundary_rho=(rho_max+average_rho)/2
        dots_with_high_rho=dots_within_square.query('rho>@boundary_rho')
    #eles using the rho calculated already
    else:
        #calculate_boundary_rho
        average_rho=find_average_rho(dots_within_square, dc)
        rho_max = dot[4]
        boundary_rho=(rho_max+average_rho)/2
        dots_with_high_rho=dots_within_square.query('rho>@boundary_rho')

    
    if len(dots_with_high_rho) == 1:
        #for the dot is solo within ranges
        return dots_with_high_rho.iloc[0,0], dots_with_high_rho.iloc[0,1], 0, 0
    else:
        #drop outline out
        dwhr_os = dots_with_high_rho.values[:,0:2]  # dwhr_os is shorten for dots_with_high_rho only_site
        dst = distance.pdist(dwhr_os)
        dst_square = distance.squareform(dst)
        #对每个点，若其对其它点的平均距离大于所有点的平均距离*1.8，就不要了。
        T_F_of_remain = dst_square.sum(axis=1) / (len(dst_square) -1) <= dst.mean() * 1.8
        dots_with_high_rho = dots_with_high_rho.loc[T_F_of_remain,:]

        #get border and new center
        border_x_min = min(dots_with_high_rho.start1)
        border_x_max = max(dots_with_high_rho.start1)
        border_y_min = min(dots_with_high_rho.start2)
        border_y_max = max(dots_with_high_rho.start2)
        center_x = (border_x_max + border_x_min)/2
        center_y = (border_y_max + border_y_min)/2
        side_length_x = border_x_max - border_x_min
        side_length_y = border_y_max - border_y_min

        return center_x, center_y, side_length_x, side_length_y


#determine whether the left square and the right square is equal in density, then, the same to the vertical.
#if they are not equal, like, fold change larger than 2, then, compare with the single square, not the mean of the vertical or horizontal
def horizontal_verticalfiltor(dot, dots):
    smal_x = dot[10]/2
    smal_y = dot[11]/2
    lage_x = smal_x*2.5
    lage_y = smal_y*2.5
    #small square and large square
    small_square=sum(dots.query('@dot[8]-@smal_x<start1<@dot[8]+@smal_x and @dot[9]-@smal_y<start2<@dot[9]+@smal_y').counts)
    large_square=sum(dots.query('@dot[8]-@lage_x<start1<@dot[8]+@lage_x and @dot[9]-@lage_y<start2<@dot[9]+@lage_y').counts)-small_square
    saml_to_lar = (lage_x*lage_y/(smal_x*smal_y)-1)*small_square/(large_square+0.0001)
    #saml_to_lar = 5.25*small_square/(large_square+0.0001)  is the same
    #    return small_density/large_density    #get fold_change

    #vertical square and horizontal square
    vertical_square1 = sum(dots.query('@dot[8]-@smal_x<start1<@dot[8]+@smal_x and @dot[9]+@smal_y<start2<@dot[9]+3*@smal_y').counts)
    vertical_square2 = sum(dots.query('@dot[8]-@smal_x<start1<@dot[8]+@smal_x and @dot[9]-3*@smal_y<start2<@dot[9]-@smal_y').counts)
    horizontal_square1 = sum(dots.query('@dot[8]+@smal_x<start1<@dot[8]+3*@smal_x and @dot[9]-@smal_y<start2<@dot[9]+@smal_y').counts)
    horizontal_square2 = sum(dots.query('@dot[8]-3*@smal_x<start1<@dot[8]-@smal_x and @dot[9]-@smal_y<start2<@dot[9]+@smal_y').counts)
    vertical_ratio = vertical_square2/(vertical_square1 + 0.0001)
    horizontal_ratio = horizontal_square2/(horizontal_square1 + 0.0001)
    #if ratio of vertical squares is too large or too small, choose the small fc as real fc
    if vertical_ratio > 2 or vertical_ratio < 0.05:
        smal_to_verti = min(small_square/(vertical_square1 + 0.0001), small_square/(vertical_square2 + 0.0001))
    else:
        smal_to_verti = small_square/(vertical_square1 + vertical_square2 + 0.0001)*2
    if horizontal_ratio > 2 or horizontal_ratio < 0.05:
        smal_to_horiz = min(small_square/(horizontal_square1 + 0.0001), small_square/(horizontal_square2 + 0.0001))
    else:
        smal_to_horiz = small_square/(horizontal_square1 + horizontal_square2 +0.0001)*2

    if any(i==0 for i in [vertical_square1, vertical_square2, horizontal_square1, horizontal_square2]):
        saml_to_lar = saml_to_lar/2
        smal_to_verti = smal_to_verti/2
        smal_to_horiz = smal_to_horiz/2

    return saml_to_lar, smal_to_verti, smal_to_horiz
