import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from abc import ABC, abstractmethod
from typing import List, Dict
import math
import warnings


class Figure(ABC):
    def __init__(self):
        pass

    def _order_coordinates(self, x, y):
        x, y = np.array(x), np.array(y)
        order = np.argsort(np.arctan2(y - y.mean(), x - x.mean()))
        return x[order], y[order]

    def plot(self, ax, left_center_pts, right_center_pts, widths, color):
        xs, ys = self.get_coordinates(left_center_pts, right_center_pts, widths)
        sorted_xs, sorted_ys = zip(*[self._order_coordinates(x, y) for x, y in zip(xs, ys)])
        for x, y in zip(sorted_xs, sorted_ys):
            ax.fill(x, y, color)

        return ax

    @abstractmethod
    def get_coordinates(self, left_center_pts, right_center_pts, widths):
        pass

    def get_center_highlight(self, xs, ys, ratio_color_centers):

        color_left_center_pts, color_right_center_pts = [], []

        for x, y, r in zip(xs, ys, ratio_color_centers):
            e_x = x[0] - x[1]
            e_y = y[0] - y[1]

            color_left_center = (x[1] + e_x * r, y[1] + e_y * r)
            color_right_center = (x[3] + e_x * r, y[3] + e_y * r)

            color_left_center_pts.append(color_left_center)
            color_right_center_pts.append(color_right_center)

        return color_left_center_pts, color_right_center_pts


class Parallelogram(Figure):
    def __init__(self):
        super().__init__()

    def get_coordinates(self, left_center_pts, right_center_pts, widths):
        xs, ys = [], []
        for l, r, w in zip(left_center_pts, right_center_pts, widths):
            x, y = np.zeros(4), np.zeros(4)
            alpha = np.arctan(abs(l[1] - r[1]) / abs(l[0] - r[0])) if l[0] != r[0] else np.arctan(np.inf)
            vertical_w = w / np.cos(alpha)

            x[0:2], x[2:4] = l[0], r[0]
            y[0], y[1], y[2], y[3] = l[1] + vertical_w / 2, l[1] - vertical_w / 2, \
                                     r[1] + vertical_w / 2, r[1] - vertical_w / 2

            xs.append(x)
            ys.append(y)

        return xs, ys


class Rectangle(Figure):
    def __init__(self):
        super().__init__()

    def get_coordinates(self, left_center_pts, right_center_pts, widths):
        xs, ys = [], []
        for l, r, w in zip(left_center_pts, right_center_pts, widths):
            x, y = np.zeros(4), np.zeros(4)
            alpha = np.arctan(abs(l[1] - r[1]) / abs(l[0] - r[0])) if l[0] != r[0] else np.arctan(np.inf)
            vertical_w = w / np.cos(alpha)

            ax, ay = l[0], l[1] + vertical_w / 2

            cx = ax + w * np.sin(alpha)
            cy = ay - w * np.cos(alpha)

            ex = ax + w * np.sin(alpha) / 2
            ey = ay - w * np.cos(alpha) / 2

            new_ax = ax + l[0] - ex
            new_ay = ay + l[1] - ey

            new_cx = cx + l[0] - ex
            new_cy = cy + l[1] - ey

            x[0], x[1] = new_ax, new_cx
            y[0], y[1] = (new_ay, new_cy) if l[1] <= r[1] else (new_cy, new_ay)

            x[2], x[3] = x[0] + r[0] - l[0], x[1] + r[0] - l[0]
            y[2], y[3] = y[0] + r[1] - l[1], y[1] + r[1] - l[1]

            xs.append(x)
            ys.append(y)

        return xs, ys


class Hammock:
    def __init__(self,
                 # main
                 data_df: pd.DataFrame = None,
                 ):

        # assertions
        if data_df.empty:
            raise ValueError(
                f'data must be provided. '
            )

        self.data_df_origin = data_df
        self.missing_data_placeholder = "missing_data_placeholder_MDP"
        self.color_coloumn_placeholder = "value_color_col_placeholder_VCCP"
        self.same_var_placeholder = "_same_var_placeholder_SVP_"

        # to resolve same_scale and value_order alignment issue
        self.same_scale_placeholder = "_same_scale_placeholder_SSP_"

    def plot(self,
             var: List[str] = None,
             value_order: Dict[str, Dict[int, str]] = None,
             missing: bool = False,
             hi_missing: bool = False,
             missing_label_space: float = 1.,
             label: bool = True,
             # Highlighting
             hi_var: str = None,
             hi_value: List[str] = None,
             hi_box: str = "vertical",
             color: List[str] = None,
             default_color="lightskyblue",
             # Manipulating Spacing and Layout
             bar_width: float = 1.,
             min_bar_width: float = .1,
             space: float = .5,
             label_options: Dict = None,
             height: float = 10.,
             width: float = 15.,
             # Other options
             shape: str = "rectangle",
             same_scale: List[str] = None,
             display_figure: bool = True,
             save_path: str = None,
             ):

        var_lst = var
        # parse the color input to enable intensity feature
        color_lst = self._parse_colors(color)
        self.data_df = self.data_df_origin.copy()
        for col in self.data_df:
            if self.data_df[col].dtype.name == "category":
                self.data_df[col] = self.data_df[col].cat.add_categories(self.missing_data_placeholder)
            elif "float" in self.data_df[col].dtype.name:
                self.data_df[col] = self.data_df[col].apply(lambda x: np.round(x, 2))
        self.data_df_columns = self.data_df.columns.tolist()

        if not var_lst:
            raise ValueError(
                f'There must be some variable names passed to the argument "var".'
            )

        if color and type(color) != type([]):
            raise ValueError(
                f'Argument "color" must be a list os str.'
            )

        if same_scale and not set(same_scale) <= set(self.data_df_columns):
            error_values = (set(same_scale) ^ set(self.data_df_columns)) & set(same_scale)
            raise ValueError(
                f'the variables: {error_values} in var_lst is not in data or value names user given does not match the data '
            )

        if not set(var_lst) <= set(self.data_df_columns):
            error_values = (set(var_lst) ^ set(self.data_df_columns)) & set(var_lst)
            raise ValueError(
                f'the variables: {error_values} in var_lst is not in data or value names user given does not match the data '
            )

        if value_order:
            for k, v_ori in value_order.items():
                uni_val_set = set(self.data_df[k].dropna().unique())
                v = [value_name for order, value_name in v_ori.items()]
                if not set(v) >= uni_val_set:
                    error_values = (set(v) ^ uni_val_set) & set(v)
                    raise ValueError(
                        f'Does not find values {error_values} in variable {k}.'
                    )

        if hi_var and not hi_var in self.data_df_columns:
            raise ValueError(
                f'highlight variable is not in data. '
            )

        if hi_var and not set(var_lst) <= set(self.data_df_columns):
            error_values = (set(var_lst) ^ set(self.data_df_columns)) & set(var_lst)
            raise ValueError(
                f'the variables: {error_values} in var_lst is not in data.'
            )

        if hi_var and not (hi_value or missing):
            raise ValueError(
                f'hi_value must be speicified as hi_var is given.'
            )

        self.var_lst = self._label_same_varname(var_lst)
        self.value_order = value_order
        self.missing = missing
        self.hi_missing = hi_missing
        self.missing_label_space = missing_label_space
        self.label = label
        # Highlighting
        self.hi_var = hi_var
        self.hi_value = hi_value
        if self.missing and self.hi_missing:
            # self.hi_value = [x if x!="missing" else self.missing_data_placeholder for x in hi_value]
            if self.hi_value:
                self.hi_value.append(self.missing_data_placeholder)
            else:
                self.hi_value = [self.missing_data_placeholder]
        colors = ["red", "green", "yellow", "purple", "orange", "gray", "brown", "olive", "pink", "cyan", "magenta"]
        self.color_lst = [color for color in color_lst] if color_lst else (
            colors[:len(self.hi_value)] if hi_var else None)
        if hi_var:
            if hi_value and len(self.color_lst) < len(hi_value):
                for i in range(len(hi_value) - len(self.color_lst)):
                    for c in colors:
                        if c not in self.color_lst:
                            self.color_lst.append(c)
                            break
                warnings.warn(
                    f"Warning: The length of color is less than the total number of (high values and missing), color was automatically extended to {self.color_lst}")
        if hi_var and default_color in self.color_lst:
            raise ValueError(
                f'The current highlight colors {self.color_lst} conflict with the default color {default_color}. Please choose another default color or other highlight colors'
            )
        # Manipulating Spacing and Layout
        self.bar_width = bar_width
        self.min_bar_width = min_bar_width
        self.space = space
        self.label_options = label_options
        self.height = height
        self.width = width
        # Other options
        self.shape = shape
        self.same_scale = same_scale

        if self.missing:
            self.data_df = self.data_df.fillna(self.missing_data_placeholder)
        else:
            self.data_df = self.data_df.dropna()

        if hi_var:
            hi_var_unique_set = set(self.data_df[hi_var].unique())
            hi_var_unique_set.add(self.missing_data_placeholder)

            if not set(self.hi_value) <= hi_var_unique_set:
                error_values = (set(self.hi_value) ^ hi_var_unique_set) & set(self.hi_value)
                raise ValueError(
                    f'the values: {error_values} in highlight value is not in data.'
                )

            value_color_dict = dict(zip(self.hi_value, self.color_lst))

            self.data_df[self.color_coloumn_placeholder] = self.data_df[hi_var].apply(
                lambda x: value_color_dict[x] if value_color_dict.get(x) else default_color)
            self.color_lst.append(default_color)
            self.color_lst.reverse()

        # count unique pairs of the input var_lst
        var_pairs = self._get_two_var(self.var_lst)

        pair_dict_lst = []
        pair_dict_lst_color = []
        data_point_numbers = []
        for p in var_pairs:
            varname_p = [self._get_varname(var) for var in p]
            pair_dict_temp = self.data_df.groupby(varname_p, observed=True).size().to_dict()
            pair_dict = {}
            for k, v in pair_dict_temp.items():
                if v == 0:
                    continue
                pair_dict[((p[0], k[0]), (p[1], k[1]))] = v
                data_point_numbers.append(v)
            pair_dict_lst.append(pair_dict)

        if hi_var:
            pair_dict_lst_color = []
            for p in var_pairs:
                varname_p = [self._get_varname(var) for var in p]
                varname_p.append(self.color_coloumn_placeholder)
                color_dict_temp = self.data_df.groupby(varname_p, observed=True).size().to_dict()
                color_dict = {}
                for k, v in color_dict_temp.items():
                    if v == 0:
                        continue
                    if not color_dict.get(((p[0], k[0]), (p[1], k[1]))):
                        color_dict[((p[0], k[0]), (p[1], k[1]))] = {}
                    color_dict[((p[0], k[0]), (p[1], k[1]))][k[2]] = v
                pair_dict_lst_color.append(color_dict)

        fig, ax = plt.subplots(figsize=(self.width, self.height))
        ax, coordinates_dict = self._list_labels(ax, self.height, self.width, self.label)

        space = self.space * 10 if label else 0
        # when space set to 1, change to univariate mode
        space_univar = True if space == 10 else False
        bar = self.bar_width * 3.5 / max(data_point_numbers)

        if self.shape == "parallelogram":
            figure_type = Parallelogram()
        elif self.shape == "rectangle":
            figure_type = Rectangle()

        widths, left_center_pts, right_center_pts = [], [], []
        for col in pair_dict_lst:
            for k, v in col.items():
                left_label = k[0]
                right_label = k[1]
                width = bar * v
                if self.min_bar_width and width <= self.min_bar_width:
                    width = self.min_bar_width
                left_coordinate = (coordinates_dict[left_label][0] + space, coordinates_dict[left_label][1])
                right_coordinate = (coordinates_dict[right_label][0] - space, coordinates_dict[right_label][1])
                widths.append(width)

                left_center_pts.append(left_coordinate)
                right_center_pts.append(right_coordinate)

        label_rectangle = True if self.label else False
        label_rectangle_default_color = default_color
        label_rectangle_widths = []
        label_rectangle_total_obvs = {}
        
        label_rectangle_vertical = True if hi_box == "vertical" else False

        if label_rectangle:
            label_rectangle_painter = Rectangle()
            label_rectangle_left_center_pts, label_rectangle_right_center_pts = [],[]
            for k,v in coordinates_dict.items():

                # get width for label rectangles by counting the number of observations for each value

                col_name = k[0].split(self.same_var_placeholder)[0]
                num_obv = self.data_df[col_name].value_counts().get(k[1], 0)
                label_rectangle_total_obvs[k] = num_obv
                label_rectangle_width = bar * num_obv
                if self.min_bar_width and label_rectangle_width <= self.min_bar_width:
                    label_rectangle_width = self.min_bar_width

                # get left and right coordinates for label rectangles
                # add space for very thick label rectangles 
                half_label_rectangle_width = label_rectangle_width/2
                edge_adjust = self.max_y_range * 0.01
                if v[1] - half_label_rectangle_width < 0:
                    adjust_value = half_label_rectangle_width - v[1] + edge_adjust
                    label_rectangle_left_coordinate= (v[0]-space*0.8, v[1]+adjust_value)
                    label_rectangle_right_coordinate = (v[0] + space * 0.8, v[1]+adjust_value)
                elif v[1] + half_label_rectangle_width > self.max_y_range:
                    adjust_value = half_label_rectangle_width + v[1] - self.max_y_range + edge_adjust
                    label_rectangle_left_coordinate= (v[0]-space*0.8, v[1]-adjust_value)
                    label_rectangle_right_coordinate = (v[0] + space * 0.8, v[1]-adjust_value)
                else:
                    label_rectangle_left_coordinate = (v[0]-space*0.8, v[1])
                    label_rectangle_right_coordinate = (v[0] + space * 0.8, v[1])

                label_rectangle_left_center_pts.append(label_rectangle_left_coordinate)
                label_rectangle_right_center_pts.append(label_rectangle_right_coordinate)

                
                
                label_rectangle_widths.append(label_rectangle_width)

        if not hi_var:
            if not space_univar:
                ax = figure_type.plot(ax, left_center_pts, right_center_pts, widths, default_color)
            if label_rectangle:
                ax = label_rectangle_painter.plot(ax, label_rectangle_left_center_pts, label_rectangle_right_center_pts, label_rectangle_widths,label_rectangle_default_color)
        else:
            width_color_total = [0] * len(widths)
            label_rectangle_width_color_total = [0] * len(coordinates_dict)
            xs, ys = figure_type.get_coordinates(left_center_pts, right_center_pts, widths)
            if not space_univar:
                
                for color in self.color_lst:
                    widths_color, ratio_color_centers = [], []
                    index = 0
                    for col in pair_dict_lst_color:
                        for k, v in col.items():
                            left_label = k[0]
                            right_label = k[1]
                            if v.get(color):
                                width_temp = bar * v.get(color)
                                if self.min_bar_width and width_temp <= self.min_bar_width:
                                    width_temp = self.min_bar_width
                            else:
                                width_temp = 0

                            widths_color.append(width_temp)
                            ratio_color_centers.append((width_color_total[index] + width_temp / 2) / widths[index])
                            width_color_total[index] += width_temp
                            index += 1

                    color_left_center_pts, color_right_center_pts = figure_type.get_center_highlight(xs, ys,
                                                                                                    ratio_color_centers)
                    ax = figure_type.plot(ax, color_left_center_pts, color_right_center_pts, widths_color, color)

            # always remember that color list was reversed, so the first color is the default color
            if label_rectangle:
                # if not label_rectangle_vertical:
                label_rectangle_total_obvs_color = label_rectangle_total_obvs.copy()
                for i,color in enumerate(reversed(self.color_lst)):
                    the_hi_value = self.hi_value[i] if i != len(self.color_lst)-1 else None
                    label_rectangle_widths_color, label_rectangle_ratio_color_centers = [], []
                    idx=0
                    for k,v in coordinates_dict.items():
                        col_name = k[0].split(self.same_var_placeholder)[0]
                        # case1: hi_value and hi_var
                        if k[1] == the_hi_value and self.hi_var == col_name:
                            label_rectangle_width_temp = label_rectangle_widths[idx]
                            label_rectangle_total_obvs_color[k] = 0
                        # case2: for other variables
                        elif the_hi_value != None:
                            num_obv = self.data_df.groupby([self.hi_var, col_name], observed=True).size().get((the_hi_value, k[1]), 0)
                            label_rectangle_width_temp = bar * num_obv
                            # if self.min_bar_width and label_rectangle_width_temp <= self.min_bar_width and label_rectangle_width_temp != 0:
                            #     label_rectangle_width_temp = self.min_bar_width
                            label_rectangle_total_obvs_color[k] -= num_obv
                        # case3: for the last default color
                        else:
                            label_rectangle_width_temp = bar * label_rectangle_total_obvs_color[k]
                            # if self.min_bar_width and label_rectangle_width_temp <= self.min_bar_width and label_rectangle_width_temp != 0:
                            #     label_rectangle_width_temp = self.min_bar_width
                        label_rectangle_widths_color.append(label_rectangle_width_temp)
                        label_rectangle_ratio_color_centers.append((label_rectangle_width_color_total[idx] + label_rectangle_width_temp / 2) / label_rectangle_widths[idx])
                        label_rectangle_width_color_total[idx] += label_rectangle_width_temp
                        idx+=1
                    if not label_rectangle_vertical:
                        xs, ys = label_rectangle_painter.get_coordinates(label_rectangle_left_center_pts, label_rectangle_right_center_pts, label_rectangle_widths)
                        color_left_center_pts, color_right_center_pts = label_rectangle_painter.get_center_highlight(xs, ys,
                                                                                                    label_rectangle_ratio_color_centers)
                        ax = label_rectangle_painter.plot(ax, color_left_center_pts, color_right_center_pts, label_rectangle_widths_color, color)
                        # ax = label_rectangle_painter.plot(ax, label_rectangle_left_center_pts, label_rectangle_right_center_pts, label_rectangle_widths,'green')
                    else:
                        xs, ys = label_rectangle_painter.get_coordinates(label_rectangle_left_center_pts, label_rectangle_right_center_pts, label_rectangle_widths)

                        # switch the order of xs and ys temporarily for calculating the vertical coordinates
                        vertical_xs = [np.array([x[1],x[3],x[0],x[2]]) for x in xs]
                        vertical_ys = [np.array([y[1],y[3],y[0],y[2]]) for y in ys]

                        vertical_color_left_center_pts, vertical_color_right_center_pts = label_rectangle_painter.get_center_highlight(vertical_xs, vertical_ys,
                                                                                                    label_rectangle_ratio_color_centers)
                        # switch back to normal coordinates
                        vertical_label_rectangle_widths_color = [space*0.8*2*(w_color/w) for w_color,w in zip (label_rectangle_widths_color, label_rectangle_widths)]
                        vertical_color_left_center_pts, vertical_color_right_center_pts, vertical_label_rectangle_widths_color = self._compute_left_right_centers(
                            vertical_color_left_center_pts, vertical_color_right_center_pts, vertical_label_rectangle_widths_color
                        )


                        ax = label_rectangle_painter.plot(ax, vertical_color_left_center_pts, vertical_color_right_center_pts,vertical_label_rectangle_widths_color, color)


                # else:
                #     vertical_label_rectangle_left_center_pts = [(pt2[0],pt1[0]) for pt1, pt2 in zip(label_rectangle_left_center_pts,label_rectangle_right_center_pts)]
                #     vertical_label_rectangle_right_center_pts = [(pt1[1],pt2[0]) for pt1, pt2 in zip(label_rectangle_left_center_pts,label_rectangle_right_center_pts)]

                #     label_rectangle_total_obvs_color = label_rectangle_total_obvs.copy()
                #     for i,color in enumerate(reversed(self.color_lst)):

        if display_figure:
            ax.get_figure()
        else:
            plt.close()

        if save_path:
            ax.get_figure().savefig(save_path)

        return ax

    def _get_varname(self, x):
        return x.split(self.same_var_placeholder)[:-1][0]

    def is_float(self, element: any) -> bool:
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def _label_same_varname(self, var_lst: List[str]):
        sorted_index = np.argsort(var_lst)
        unsorted_index = np.argsort(sorted_index)
        sorted_var_lst = sorted(var_lst)
        sorted_var_lst = [var + self.same_var_placeholder for var in sorted_var_lst]
        for i in range(len(sorted_var_lst) - 1):
            if self._get_varname(sorted_var_lst[i]) == self._get_varname(sorted_var_lst[i + 1]):
                sorted_var_lst[i + 1] += str(i + 1)

        unsorted_var_lst = [sorted_var_lst[i] for i in unsorted_index]
        return unsorted_var_lst

    def _get_two_var(self, var_lst: List[str]):

        var_pair_lst = []

        for i in range(len(var_lst) - 1):
            var_pair_lst.append([var_lst[i], var_lst[i + 1]])

        return var_pair_lst

    def _gen_coordinate(self, start, n, edge, spacing, total_range, val_type="str"):
        coor_lst = []

        if val_type == "str":
            for i in range(n):
                coor_lst.append(start + i * spacing)

            coor_lst.append(total_range + (start - edge) - edge)
        else:
            for val in spacing:
                coor_lst.append(start + val)

            coor_lst.append(total_range + (start - edge) - edge)
        return coor_lst

    # using the variable with the largest number of values as the criteria for same_scale
    def _get_same_scale_minmax(self, original_unique_value):
        min, max = 0, 0
        for i, varname in enumerate(self.same_scale):
            var_type = str(self.data_df_origin[varname].dtype.name)
            if "int" in var_type or "float" in var_type:
                min_val, max_val = original_unique_value[varname][0], original_unique_value[varname][-1]
                if i == 0:
                    min, max = min_val, max_val
                else:
                    min = min_val if min_val < min else min
                    max = max_val if max_val > max else max

            else:
                min_val, max_val = 1, len(original_unique_value[varname])
                if i == 0:
                    min, max = min_val, max_val
                else:
                    min = min_val if min_val < min else min
                    max = max_val if max_val > max else max
        return (min, max)

    def _list_labels(self, ax, figsize_y, figsize_x, label):

        scale = 10
        edge_scale = 10
        y_range = scale * figsize_y - self.missing_label_space * scale if self.missing else scale * figsize_y
        x_range = scale * figsize_x
        self.max_y_range, self.max_x_range = scale * figsize_y, scale * figsize_x
        edge_x_range = x_range / edge_scale
        edge_y_range = y_range / edge_scale
        # self.edge_y_range, self.edge_x_range = edge_y_range, edge_x_range
        y_start = edge_y_range + self.missing_label_space * scale if self.missing else edge_y_range
        coordinates_dict = {}

        unique_value = []
        original_unique_value = {}
        varname_lst = [self._get_varname(var) for var in self.var_lst]

        for var, varname in zip(self.var_lst, varname_lst):
            unique_valnames = self.data_df[varname].dropna().unique().tolist()
            sorted_unique_valnames = []
            if self.value_order and varname in self.value_order:
                varname_value_order_dict = self.value_order[varname]
                sorted_unique_valnames_temp = [v for k, v in
                                               sorted(varname_value_order_dict.items(), key=lambda item: item[0])]
                for v in sorted_unique_valnames_temp:
                    if v in unique_valnames:
                        sorted_unique_valnames.append(v)
                    else:
                        sorted_unique_valnames.append(self.same_scale_placeholder)
            if self.missing_data_placeholder in unique_valnames:
                unique_valnames.remove(self.missing_data_placeholder)
                sorted_unique_valnames = sorted(
                    unique_valnames) if not sorted_unique_valnames else sorted_unique_valnames
                original_unique_value[varname] = sorted_unique_valnames.copy()
                sorted_unique_valnames.append(self.missing_data_placeholder)
            else:
                sorted_unique_valnames = sorted(
                    unique_valnames) if not sorted_unique_valnames else sorted_unique_valnames
                original_unique_value[varname] = sorted_unique_valnames.copy()
            unique_value.append([(var, x) for x in sorted_unique_valnames])

        ax.set_xlim(0, scale * figsize_x)
        ax.set_ylim(0, scale * figsize_y)
        ax.set_yticks([])
        var_lst = self.var_lst
        label_coordinates = self._gen_coordinate(edge_x_range, len(var_lst) - 1, edge_x_range,
                                                 (x_range - 2 * edge_x_range) / (len(var_lst) - 1), x_range)
        ax.set_xticks(label_coordinates)
        ax.set_xticklabels(varname_lst)

        # prepare for same_scale variabels
        if self.same_scale:
            same_scale_min, same_scale_max = self._get_same_scale_minmax(original_unique_value)
            same_scale_range = same_scale_max - same_scale_min

        # plot labels for each variables
        for var_i, (x, uni_val) in enumerate(zip(label_coordinates, unique_value)):
            label_num = len(uni_val) - 2 if (uni_val[0][0], self.missing_data_placeholder) in uni_val else len(
                uni_val) - 1
            varname = varname_lst[var_i]
            var_type = str(self.data_df_origin[varname].dtype.name)

            # case anlysis on quant variables and string variables
            if "int" in var_type or "float" in var_type:
                temp_value_range = (y_range - 2 * edge_y_range)
                # handle the variables in same_scale
                if self.same_scale and varname in self.same_scale:
                    min_val, max_val = same_scale_min, same_scale_max
                else:
                    min_val, max_val = original_unique_value[varname][0], original_unique_value[varname][-1]
                value_interval = [temp_value_range * (x_val - min_val) / (max_val - min_val) for x_val in
                                  original_unique_value[varname]]
                uni_val_coordinates = self._gen_coordinate(y_start, label_num, edge_y_range,
                                                           value_interval, y_range, val_type="number")
            else:
                # handle the variables in same_scale
                if self.same_scale and varname in self.same_scale:
                    temp_value_range = (y_range - 2 * edge_y_range)
                    quant_val = list(range(1, len(original_unique_value[varname]) + 1))
                    min_val, max_val = same_scale_min, same_scale_max
                    value_interval = [temp_value_range * (x_val - min_val) / (max_val - min_val) for x_val in quant_val]
                    uni_val_coordinates = self._gen_coordinate(y_start, label_num, edge_y_range,
                                                               value_interval, y_range, val_type="number")
                else:
                    value_interval = (y_range - 2 * edge_y_range) / (label_num)
                    uni_val_coordinates = self._gen_coordinate(y_start, label_num, edge_y_range,
                                                               value_interval, y_range, val_type="str")

            # set coordinates for missing
            if label_num == len(uni_val) - 2:
                missing_label_index = uni_val.index((uni_val[0][0], self.missing_data_placeholder))
                uni_val_coordinates.insert(missing_label_index, edge_y_range)

            # plot labels
            for i, (val, y) in enumerate(zip(uni_val, uni_val_coordinates)):
                if val[1] == self.same_scale_placeholder:
                    continue
                if label:
                    if self.missing and val[1] == self.missing_data_placeholder:
                        ax.text(x, y, "missing", ha='center', va='center')

                    elif self.label_options and varname in self.label_options:
                        ax.text(x, y, val[1], ha='center', va='center', **self.label_options[varname])

                    else:
                        ax.text(x, y, val[1], ha='center', va='center')
                coordinates_dict[val] = (x, y)
        return ax, coordinates_dict

    def _parse_colors(self, color_list):
        """Parses a list of colors, converting 'color=alpha' format to hex with transparency."""
        parsed_colors = []
        
        if color_list is None:
            return None

        for color in color_list:
            if "=" in color:  # Handle colors with alpha values
                try:
                    color_name, alpha_str = color.split("=")  # Split color and alpha
                    alpha = float(alpha_str)  # Convert alpha to float
                    rgba = mcolors.to_rgba(color_name, alpha=alpha)  # Convert to RGBA
                    hex_color = mcolors.to_hex(rgba, keep_alpha=True)  # Convert to Hex
                    parsed_colors.append(hex_color)
                except Exception as e:
                    print(f"Warning: Invalid color format '{color}', using default color.")
                    parsed_colors.append(color_name)  # Fallback to default color
            else:
                parsed_colors.append(color)  # Add standard color names directly

        return parsed_colors

    import math

    def _compute_left_right_centers(self, midpoints_top, midpoints_bottom, lengths):
        """
        Given the top and bottom midpoints of one or more aligned rectangles, along with their width,
        compute the midpoints and lengths of the left and right centers.
        
        Parameters:
        --------
        midpoints_top : list of (float, float)
            List of top edge midpoints (Tx, Ty)
        midpoints_bottom : list of (float, float)
            List of bottom edge midpoints (Bx, By)
        length : float
            The width of the rectangles (assumed to be the same for all)
            
        Returns:
        --------
        left_midpoints : list of (float, float)
            Midpoints of the left edges
        right_midpoints : list of (float, float)
            Midpoints of the right edges
        edge_length : float
            The height of the rectangles (same for both left and right edges)
        """
        n = len(midpoints_top)
        
        left_midpoints = []
        right_midpoints = []
        edge_lengths = []
        
        for i in range(n):
            Tx, Ty = midpoints_top[i]
            Bx, By = midpoints_bottom[i]

            Ty, By = (By, Ty) if Ty < By else (Ty, By)

            length = lengths[i]
            
            # Compute the vertical edge length
            edge_length = abs(By - Ty)
            
            if length != 0:
                # Compute left and right edge midpoints
                Lmx = Tx - length / 2
                Lmy = Ty - edge_length / 2
                Rmx = Tx + length / 2
                Rmy = By + edge_length / 2
            else:
                Lmx = Tx - length / 2
                Lmy = Ty - edge_length / 2
                Rmx = Lmx
                Rmy = By + edge_length / 2
                edge_length = 0
            
            left_midpoints.append((Lmx, Lmy))
            right_midpoints.append((Rmx, Rmy))
            edge_lengths.append(edge_length)
        
        return left_midpoints, right_midpoints, edge_lengths



