"""Заготовки задач на NumPy."""

# import matplotlib.pyplot as plt
import numpy as np
from grader_contracts.numpy_tasks import (
    BinarizeInput, ChessInput, EllipseInput, MatrixInput, MatrixStatistics,
    MatrixVectorBatchInput, OneHotInput, RandomMatrixInput, RectangleInput,
    TimeSeriesInput, TimeSeriesStatistics,
)


def sum_prod(data: MatrixVectorBatchInput) -> np.ndarray:
    matrices, vectors = data.matrices, data.vectors
    if len(matrices) != len(vectors) or min(len(matrices), len(vectors)) == 0: raise ValueError
    a = np.zeros((len(vectors[0]), 1))
    for i in range(len(matrices)):
        a +=  np.asarray(matrices[i]) @ np.asarray(vectors[i])
    return a

test_data_arrays = MatrixVectorBatchInput(
    matrices=[
        np.array([[1, 2], [3, 4]]),
        np.array([[1, 0], [0, 1]])
    ],
    vectors=[
        np.array([[1], [1]]),
        np.array([[2], [3]])
    ]
)
assert np.allclose(sum_prod(test_data_arrays), np.array([[5], [10]]))
test_data_lists = MatrixVectorBatchInput(
    matrices=[
        [[1, 2], [3, 4]],
        [[1, 0], [0, 1]]
    ],
    vectors=[
        [[1], [1]],
        [[2], [3]]
    ]
)
assert np.allclose(sum_prod(test_data_lists), np.array([[5], [10]]))


def binarize(data: BinarizeInput) -> np.ndarray:
    matrix, threshold = data.matrix, data.threshold
    q = np.where(np.asarray(matrix) > threshold, 1, 0)
    return q

test_data_bin = BinarizeInput(
    [[2, 3], [0.1, 0.5]],
)
print(binarize(test_data_bin))

def unique_rows(data: MatrixInput) -> list[list[float]]:
    matrix = data.matrix
    res = []
    for i in np.asarray(matrix, dtype=float):
        res.append(np.unique(ar= i).tolist())
    return res

print(unique_rows(MatrixInput([[1.0,2.0,3.0], [3.0,3.0,8.0],[5.0,5.0,5.0]])))
def unique_columns(data: MatrixInput) -> list[list[float]]:
    matrix = data.matrix
    return unique_rows(MatrixInput(np.asarray(matrix).T))
print(unique_columns(MatrixInput([[1,3,5], [2,3,5],[3,8,5]])))



def matrix_statistics(data: RandomMatrixInput) -> MatrixStatistics:
    rows, columns, mean, std, seed = data.rows, data.columns, data.mean, data.std, data.seed
    rng = np.random.default_rng(seed)
    mx = rng.normal(size=(rows, columns), loc= mean, scale=std)
    return MatrixStatistics(mx, mx.mean(axis=1), mx.mean(axis=0), mx.var(axis=1), mx.var(axis=0))

input_data = RandomMatrixInput(rows=4, columns=5, mean=10.0, std=2.0, seed=42)
stats = matrix_statistics(input_data)

assert stats.matrix.shape == (4, 5), "Неверная форма матрицы"
assert stats.row_means.shape == (4,), "Неверное количество средних по строкам"
assert stats.column_means.shape == (5,), "Неверное количество средних по столбцам"
assert stats.row_variances.shape == (4,), "Неверное количество дисперсий по строкам"
assert stats.column_variances.shape == (5,), "Неверное количество дисперсий по столбцам"

assert np.allclose(stats.row_means, stats.matrix.mean(axis=1)), "Ошибка в row_means"
assert np.allclose(stats.column_means, stats.matrix.mean(axis=0)), "Ошибка в column_means"
assert np.allclose(stats.row_variances, stats.matrix.var(axis=1)), "Ошибка в row_variances"
assert np.allclose(stats.column_variances, stats.matrix.var(axis=0)), "Ошибка в column_variances"

stats_duplicate = matrix_statistics(input_data)
assert np.array_equal(stats.matrix, stats_duplicate.matrix), "Seed не обеспечивает повторяемость"

input_diff_seed = RandomMatrixInput(rows=4, columns=5, mean=10.0, std=2.0, seed=99)
stats_diff = matrix_statistics(input_diff_seed)
assert not np.array_equal(stats.matrix, stats_diff.matrix), "Матрицы с разным seed не должны совпадать"


def chess(data: ChessInput) -> np.ndarray:
    rows, columns, first, second = data.rows, data.columns, data.first, data.second
    mx = np.zeros((rows, columns), dtype= int)
    mx[::2, ::2] = first
    mx[1::2, 1::2] = first
    mx[1::2, ::2] = second
    mx[::2, 1::2] = second
    return mx
print(chess(ChessInput(3,4, 1, 0)))
print(chess(ChessInput(3,4, 0, 1)))



def draw_rectangle(data: RectangleInput) -> np.ndarray:
    width, height = data.width, data.height
    image_height, image_width = data.image_height, data.image_width
    shape_color, background_color = data.shape_color, data.background_color
    img = np.full((image_height, image_width, 3), background_color, dtype= np.uint8)
    padding_height = (image_height - height) // 2
    padding_width = (image_width - width) // 2
    img[padding_height : padding_height + height, padding_width : padding_width + width] = shape_color
    # plt.imshow(img)
    # plt.show()
    return img
draw_rectangle(RectangleInput(width=3,height=3,image_height=5,image_width=5, shape_color=(200,10,10), background_color=(10,200,10)))



def draw_ellipse(data: EllipseInput) -> np.ndarray:
    semi_axis_x, semi_axis_y = data.semi_axis_x, data.semi_axis_y
    image_height, image_width = data.image_height, data.image_width
    shape_color, background_color = data.shape_color, data.background_color
    img = np.full((image_height, image_width, 3), background_color, dtype= np.uint8)
    center_x = image_width // 2
    center_y = image_height // 2
    y, x = np.ogrid[:image_height, :image_width]
    mask = ((x - center_x)**2 / semi_axis_x**2 + (y - center_y)**2 / semi_axis_y**2) <= 1
    img[mask] = shape_color
    # plt.imshow(img)
    # plt.show()
    return img
draw_ellipse(EllipseInput(semi_axis_x=30,semi_axis_y=50,image_height=100,image_width=80, shape_color=(200,10,10), background_color=(10,200,10)))



def analyze_time_series(data: TimeSeriesInput) -> TimeSeriesStatistics:
    values, window = data.values, data.window
    arr = np.asarray(values)
    mean = np.mean(arr)
    var = np.var(arr)
    std = np.std(arr)
    local_max = np.where((arr[:-2] < arr[1:-1]) &(arr[1:-1] > arr[2:]))[0] + 1
    local_min = np.where((arr[:-2] > arr[1:-1]) &(arr[1:-1] < arr[2:]))[0] + 1
    windows =  np.lib.stride_tricks.sliding_window_view(arr, window)
    moving_avg = np.mean(windows, axis=-1)
    return TimeSeriesStatistics(
        mean=float(mean),
        variance=float(var),
        std=float(std),
        local_maxima_indices=local_max,
        local_minima_indices=local_min,
        moving_average=moving_avg,
    )


test_input = TimeSeriesInput(
    values=[1.0, 5.0, 2.0, 2.0, 8.0, 3.0, 7.0, 4.0],
    window=3
)

result = analyze_time_series(test_input)
print("Mean:", result.mean)
print("Var:", result.variance)
print("Std:", result.std)
print("Local Maxima indices:", result.local_maxima_indices)
print("Local Minima indices:", result.local_minima_indices)
print("Moving average:", result.moving_average)

def one_hot(data: OneHotInput) -> np.ndarray:
    labels, class_count = data.labels, data.class_count
    if class_count is None:
        class_count = np.max(labels) + 1
    arr = np.zeros((len(labels), class_count))
    arr[np.arange(len(labels)), labels] = 1
    return arr
print(one_hot(OneHotInput([0, 2, 3, 0])))

