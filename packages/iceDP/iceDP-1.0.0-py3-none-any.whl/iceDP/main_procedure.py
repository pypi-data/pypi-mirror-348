# -*- coding: utf-8 -*-



import pandas,numpy,math,multiprocessing
from functools import partial
from . import filterling



class bunchDots():
    dc = 150000    #setup real dc, the side length of the square, or the diameter of the circle
    use_multiply_in_find_rho = False
    n_cpu = 4
    window_size = 600000    #side length of filtering windows
    
        
    def readData(self, data_adress):
        self.dots = pandas.read_csv(data_adress, sep= '\t', names = ['start1','start2','counts'])
        self.x_sorted=self.dots.sort_values(by = 'start1',axis = 0,ascending = True)
        self.y_sorted=self.dots.sort_values(by = 'start2',axis = 0,ascending = True)
        self.x_sorted=self.x_sorted.reset_index()
        self.y_sorted=self.y_sorted.reset_index()
        self.x=self.x_sorted.values[:, 1]
        self.y=self.y_sorted.values[:, 2]
        
        
    def get_rho(self):
        pool=multiprocessing.Pool(processes = self.n_cpu)
        partial_find_rho = partial(find_rho, dc=self.dc, x=self.x, y=self.y, x_sorted=self.x_sorted, y_sorted=self.y_sorted,
                                dots=self.dots, use_multiply_in_find_rho = self.use_multiply_in_find_rho)
        rho = pool.map(partial_find_rho, self.dots.values)
        pool.close()
        pool.join()
        #dots.loc[:,'rho'] = rho
        self.dots = self.dots.assign(rho = rho)
        
        
    def get_delta(self, not_former = True):
        if self.use_multiply_in_find_rho == False:
            #attention here: there should have a new way to determine the min_rho
            self.min_rho = 30
        else:
            #attention here: there should have a new way to determine the min_rho
            self.min_rho = 100000
        self.rho_sorted = self.dots.sort_values(by = 'rho', axis = 0, ascending = True).reset_index()
        self.rho_sorted.rho=self.rho_sorted.rho.round()  #for normalized data, the rho is not int. And in find_delta(), the multi-processing require as much more the same rho as possible
        delta = []
        
        #  if do not want to calculate the former delta
        if not_former == True:
            rho_sorted_without_max_rho = self.rho_sorted.iloc[0:-sum(self.rho_sorted.rho == max(self.rho_sorted.rho)), ]    #in case of the max rho is less than 100000, so the max rho needs to be taken out
            for aa in range(0,max(rho_sorted_without_max_rho[rho_sorted_without_max_rho.rho <= self.min_rho ].index) + 1):
                delta.append(0)
            #  NOTICE!!  not calculate the former delta ends here, remember to delete [rho_without_max>rho_do_not_wanted] below, if need to calculate the former delta
        
        if self.use_multiply_in_find_rho == False:
            #run
            rho_uniq=self.rho_sorted.rho.unique()
            rho_without_max=rho_uniq[rho_uniq != max(rho_uniq)]
            if not_former == True:          # if do not want to calculate the former delta
                for aa in rho_without_max[rho_without_max > self.min_rho]:
                    #if not want to leave out former delta, delete [rho_without_max > self.min_rho]
                    delta = delta + find_delta(rho=aa, rho_sorted = self.rho_sorted, n_cpu = self.n_cpu, use_multiply_in_find_rho = self.use_multiply_in_find_rho)
            else:        # if need to calculate the former delta
                print('calculate all delta')
                for aa in rho_without_max:
                    delta = delta + find_delta(rho=aa, rho_sorted = self.rho_sorted, n_cpu = self.n_cpu, use_multiply_in_find_rho = self.use_multiply_in_find_rho)
        else:
            #run
            rho_uniq = self.rho_sorted.rho.unique()
            rho_without_max = rho_uniq[rho_uniq != max(rho_uniq)]
            pool=multiprocessing.Pool(processes = self.n_cpu)
            partial_find_delta = partial(find_delta, rho_sorted = self.rho_sorted, n_cpu = self.n_cpu, use_multiply_in_find_rho = self.use_multiply_in_find_rho)
            if not_former == True:          # if do not want to calculate the former delta
                delta_temp_list = pool.map(partial_find_delta, rho_without_max[rho_without_max > self.min_rho])
                #if not want to leave out former delta, delete [rho_without_max > self.min_rho]
            else:      # if need to calculate the former delta
                delta_temp_list = pool.map(partial_find_delta, rho_without_max)
                
            pool.close()
            pool.join()

            for i in delta_temp_list:
                delta = delta + i
         
        #for the rho_max point
        for a in self.rho_sorted.loc[self.rho_sorted.rho == max(rho_uniq), :].values:
            point=(self.rho_sorted.loc[:, ['start1','start2']].values)
            tempmaxdis = numpy.sqrt(numpy.array(numpy.sum((point - a[1:3])**2, axis=1), dtype='int64'))
            delta.append(max(tempmaxdis))
            
        #rho_sorted.loc[:,'delta']=delta
        self.rho_sorted = self.rho_sorted.assign(delta = delta)
        
        self.data_filted = self.rho_sorted.query('rho > @self.min_rho and delta > 1000000')
        self.data_filted = self.data_filted.query('rho/counts > 2')
        
        
    def do_chi_square_test(self):
        pool=multiprocessing.Pool(processes = self.n_cpu)
        partial_work = partial(filterling.chi_square_test, dc = self.dc, dots = self.dots)
        pvalue_and_fillN = pool.map(partial_work, self.data_filted.values)
        pool.close()
        pool.join()
        self.data_filted = self.data_filted.assign(p_value = [pvalue_and_fillN[i][0] for i in range(len(pvalue_and_fillN))])
        self.data_filted = self.data_filted.assign(fillN = [pvalue_and_fillN[i][1] for i in range(len(pvalue_and_fillN))])
        self.data_filted1 = self.data_filted.query('rho > @self.min_rho and p_value > 0.00001 and fillN > 7')
        
    
    def define_border(self):
        rangess = self.window_size #operation within 1Mb
        pool=multiprocessing.Pool(processes = self.n_cpu)
        partial_work = partial(filterling.auto_border, dots = self.dots, rangess = rangess, dc=self.dc, x=self.x, y=self.y, x_sorted=self.x_sorted, y_sorted=self.y_sorted, use_multiply_in_find_rho = self.use_multiply_in_find_rho, )
        a = pool.map(partial_work, self.data_filted1.values)
        pool.close()
        pool.join()
        #get result
        self.data_filted1 = self.data_filted1.assign(center_x=[a[i][0] for i in range(len(a))])
        self.data_filted1 = self.data_filted1.assign(center_y=[a[i][1] for i in range(len(a))])
        self.data_filted1 = self.data_filted1.assign(side_length_x=[a[i][2] for i in range(len(a))])
        self.data_filted1 = self.data_filted1.assign(side_length_y=[a[i][3] for i in range(len(a))])
        #the radius of interaction spot should within 250k and larger than 10k
        self.data_filted2 = self.data_filted1.query('10000 < side_length_x < 500000 and 10000 < side_length_x < 500000')

    def horizontal_and_vertical_fold_change(self):
        #calculate fc
        pool=multiprocessing.Pool(processes = self.n_cpu)
        partial_work = partial(filterling.horizontal_verticalfiltor, dots = self.dots)
        a = pool.map(partial_work, self.data_filted2.values)
        pool.close()
        pool.join()
        #assign them to data_filted2
        self.data_filted2 = self.data_filted2.assign(fold_change=[a[i][0] for i in range(len(a))])
        self.data_filted2 = self.data_filted2.assign(vertical_fc=[a[i][1] for i in range(len(a))])
        self.data_filted2 = self.data_filted2.assign(horizontal_fc=[a[i][2] for i in range(len(a))])
    

        
        
        

def find_index(point_xy, radius, list_xy_sorted):
    '''this function is designed to find the indices of two given numbers inside a sorted list(list_xy_sorted), where those two numbers is generated by added or subtracted an certain number(radius) to a given value(point_xy).'''
    target = point_xy - radius
    start = 0
    end = len(list_xy_sorted) - 1
    while start <= end:
        mid = (start + end) // 2
        if list_xy_sorted[mid] == target:
            end = mid
            break
        elif list_xy_sorted[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
    index1 = end + 1
    
    target = point_xy + radius
    start = 0
    end = len(list_xy_sorted) - 1
    while start <= end:
        mid = (start + end) // 2
        if list_xy_sorted[mid] == target:
            end = mid
            break
        elif list_xy_sorted[mid] < target:
            start = mid + 1
        else:
            end = mid - 1 
    index2=end
    '''return: point_xy - radius < index <= point_xy + radius'''
    '''deficiency：for array like find_index(2,1,[1,1,1,2,2,2,2,3,3,3,3]), will return [3,8], while I want [3,10].
    It will choose middle site of [3,3,3,3]'''
    return [index1,index2]


def find_lower_upper_index(point_xy, radius, list_xy_sorted):
    '''this function is to find the indices of two given numbers inside a sorted list(list_xy_sorted),
    where those two numbers is generated by added or subtracted an certain number(dc) to a given value(point_xy).'''
    target = point_xy - radius
    start = 0
    end = len(list_xy_sorted) - 1
    while start <= end:
        mid = (start + end) // 2
        if list_xy_sorted[mid] >= target:
            end = mid - 1
        else:
            start = mid + 1
        #print(start,mid,end)
    index1 = end+1

    target = point_xy + radius
    start = 0
    end = len(list_xy_sorted) - 1
    while start <= end:
        mid = (start + end) // 2
        #print(start,mid,end)
        if list_xy_sorted[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
    index2 = end
    '''return: point_xy - radius <= index < point_xy + radius'''
    return [index1,index2]


def which_y(dot_y, y_upper):
    if dot_y < y_upper[0]:
        return 'a'
    elif dot_y < y_upper[1]:
        return 'b'
    elif dot_y <= y_upper[2]:
        return 'c'


def find_rho(point, dc, x, y, x_sorted, y_sorted, use_multiply_in_find_rho,dots):
    '''find rho by separating the square into 9 small squres, then multiplying the density of small squares'''
    dc = dc/6
    if use_multiply_in_find_rho == True:
        '''
        For every small squres, find the counts by using find_index, then, multiply those counts.
        
        multiplied_density=1
        for i in (-2*dc,0,2*dc):
            xind=find_index(point[0]+i,dc,x)
            for ii in (-2*dc,0,2*dc):
                yind=find_index(point[1]+ii,dc,y)
                density_smallsquare=sum(y_sorted.loc[yind[0]:yind[1]]['index'].isin(x_sorted.loc[xind[0]:xind[1]]['index']))
                multiplied_density=multiplied_density*(density_smallsquare+1)
                #print(multiplied_density)
        return multiplied_density
        
        Need to use find_index 9 times, costing some times, so, improvement is below.
        '''
        '''the main idea is firstly, find all points within the square with side length of 6*dc, by using find_index function.
        secondly, for every point within that square, determine which small square of nine('aa' to 'cc') it belong to.
        finally,multiply all the point counts of small square of nine, which is stored in my_dict'''
        #find all points within the square with side length of 6*dc
        xind = find_lower_upper_index(point[0], 3*dc, x)
        index_x = x_sorted.loc[xind[0]:xind[1]]['index']
        yind = find_lower_upper_index(point[1], 3*dc, y)
        index_y = y_sorted.loc[yind[0]:yind[1]]['index']
        index_in_square = list(set(index_x).intersection(set(index_y)))
        dots_in_square = dots.loc[index_in_square]
        #define boundary of nine small squares
        x_upper = []
        #x_lower = []
        y_upper = []
        #y_lower = []
        for i in (-2*dc,0,2*dc):
            x_center = point[0] + i
            y_center = point[1] + i
            x_upper = x_upper + [x_center + dc]
            #x_lower = x_lower + [x_center - dc]
            y_upper = y_upper + [y_center + dc]
            #y_lower = y_lower + [y_center - dc]
        #store the counts of nine small squares in a dict
        my_dict = {'aa': 1, 'ab': 1, 'ac': 1,
                'ba': 1, 'bb': 1, 'bc': 1,
                'ca': 1, 'cb': 1, 'cc': 1,}
        #decide which small square does the point comes from.
        for i in range(len(dots_in_square)):
            dot_x = dots_in_square.iloc[i].start1
            dot_y = dots_in_square.iloc[i].start2
            dot_pair = dots_in_square.iloc[i].counts
            if dot_x < x_upper[0]:
                my_dict['a'+which_y(dot_y, y_upper)] += dot_pair
            elif dot_x < x_upper[1]:
                my_dict['b'+which_y(dot_y, y_upper)] += dot_pair
            elif dot_x <= x_upper[2]:
                my_dict['c'+which_y(dot_y, y_upper)] += dot_pair
        #multiply the number to point in each square
        multiplied_density = 1
        for key in my_dict:
            multiplied_density = multiplied_density * my_dict[key]
        return multiplied_density
    
    #-------------this is for a large square density calculated just by counting the numbers of dot within that large square----------
    else:
        xind = find_lower_upper_index(point[0],3*dc,x)
        index_x = x_sorted.loc[xind[0]:xind[1]]['index']
        yind = find_lower_upper_index(point[1],3*dc,y)
        index_y = y_sorted.loc[yind[0]:yind[1]]['index']
        index_in_square = list(set(index_x).intersection(set(index_y)))
        dots_in_square = dots.loc[index_in_square]
        return sum(dots_in_square.counts)
    #---------------end----------------
    

#define delta finding function
def calculate_dist(aa,points):
    squareofdist = numpy.sum((points - aa[1:3])**2, axis = 1)     #sometimes it willreturn an ndarray with dtype of 'object', which can't be recognized by numpy.sqrt.
    tempdis = numpy.sqrt(numpy.array(squareofdist,dtype = 'int64'))  #so, we need to change the dtype into 'int64'
    return min(tempdis)


def find_delta(rho, rho_sorted, n_cpu, use_multiply_in_find_rho=False):
    '''the difference between those two method is that, method1 pooling the same rho, while method2 pooling
    different rho, which means when there are a lot of rho is the same, then method1 is more fit. when there
    are a lot of different rho, then method2 is more fit. If there are a lot of different rho, meanwhile the
    same rho have many copys, then, method3 is more fit, which is not been completed.'''
    #method1
    if use_multiply_in_find_rho == False:
        matrix = rho_sorted[rho_sorted.rho == rho]        #get all the points that has the equal rho
        point = rho_sorted.loc[max(matrix.index) + 1:, ['start1','start2']].values       #get all the points whose rho are larger
        if len(matrix)>2:                      #if the number of point is less then 4, than pooling is not needed
            #shortage of this method, is, if there are not a bundle of same rhos, then multi-core will not be used.
            pool = multiprocessing.Pool(processes = min(len(matrix), n_cpu))
            partial_dist = partial(calculate_dist, points = point)
            delta_temp = pool.map(partial_dist, matrix.values)      #then, calculate all dist, return the minimum dist
            pool.close()
            pool.join()
        else:
            delta_temp = []
            for dot in matrix.values:
                delta_temp.append(calculate_dist(dot, point))
        return delta_temp
    else:
    #method2
        matrix = rho_sorted[rho_sorted.rho == rho]
        point = rho_sorted.loc[max(matrix.index)+1:, ['start1', 'start2']].values
        delta_temp = [calculate_dist(matrix.values[ii], point) for ii in range(len(matrix))]
        return delta_temp


def save_reult(bunchDots, filepath):
    if bunchDots.use_multiply_in_find_rho == True:
        bunchDots.min_rho = 262144
    data_filted = bunchDots.data_filted2.query('rho > @bunchDots.min_rho and fold_change > 2 and vertical_fc > 1.5 and horizontal_fc > 1.5')       #final filter

    #oueput
    data_filted.to_csv(filepath, index = False)
    print('all done!')
    #parameters can be tuned: dc     rho_min     lage      p_value     fold_change


