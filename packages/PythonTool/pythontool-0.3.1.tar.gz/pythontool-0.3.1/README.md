# 导入 Import

```python
from PythonTool import *
```

`PythonTool`依赖库：`manim`、`typing`。

The `PythonTool` dependency libraries: `manim`, `typing`.

***发现任何bug或问题，请反馈到tommy1008@dingtalk.com，谢谢！** 

***If you find any bugs or issues, please report them to tommy1008@dingtalk.com, thank you!**

```bash
pip install --upgrade PythonTool
```

记得更新`PythonTool`！

Remember to update `PythonTool`!

---

## Manim工具 Manim Tool

了解更多详情，请前往[Manim Community](https://www.manim.community)。

For more details, visit [Manim Community](https://www.manim.community).

### 公式与图形 Formulas and Graphics

```python
def ChineseMathTex(*texts, font="SimSun", tex_to_color_map={}, **kwargs):
```

创建中文数学公式，在此函数的公式部分和`tex_to_color_map`中直接写入中文即可，无需包裹`\text{}`，返回`MathTex`。`font`，设置公式中的中文字体。所有原版`MathTex`参数都可使用。

Creates Chinese mathematical formulas. You can directly write Chinese characters in the formula part of this function and in `tex_to_color_map` without wrapping them in `\text{}`. Returns `MathTex`. The `font` parameter sets the Chinese font for the formula. All original parameters of `MathTex` can be used.

```python
def YellowLine(**kwargs):
```

创建黄色的`Line`，所有原版参数都可使用。

Creates a yellow `Line`. All original parameters can be used.

```python
def LabelDot(dot_label, dot_pos, label_pos=DOWN, buff=0.1):
```

创建一个带有名字的点，返回带有点和名字的`VGroup`。`dot_label`，点的名字，字符串。`dot_pos`，点的位置，位置列表`[x,y,z]`。`label_pos`，点的名字相对于点的位置，Manim中的八个方向。`buff`，点的名字与点的间距，数值。

Creates a point with a name. Returns a `VGroup` containing the point and its name. `dot_label` is the name of the point (a string). `dot_pos` is the position of the point (a list `[x, y, z]`). `label_pos` is the position of the label relative to the point (one of the eight directions in Manim). `buff` is the spacing between the label and the point (a numerical value).

```python
def MathTexLine(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
def MathTexBrace(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
def MathTexDoublearrow(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
```

创建可以标注内容的图形，返回带有图形和标注内容的`VGroup`。`mathtex`，标注的公式，`MathTex`类型。`direction`，标注内容相对于线的位置，Manim中的八个方向。`buff`，标注内容与图形的间距，数值。图形的所有原版参数都可使用。

Creates graphics that can annotate content. Returns a `VGroup` containing the graphic and the annotation. `mathtex` is the formula to be annotated (of type `MathTex`). `direction` is the position of the annotation relative to the line (one of the eight directionsin Manim). `buff` is the spacing between the annotation and the graphic (a numerical value). All original parameters of the graphics can be used.

```python
def ExtendedLine(line: Line, extend_distance: float) -> Line:
```

将一条线延长`extend_distance`的距离，返回延长后的`Line`。`line`，`Line`类型。`extend_distance`，要延长的距离，数值。

Extends a line by `extend_distance`. Returns the extended `Line`. `line` must be of type `Line`. `extend_distance` is the distance to extend (a numerical value).

### 交点 Intersection Points

```python
def CircleInt(circle1, circle2):
```

寻找两个圆的两个交点并返回`Dot`，如果没有交点会返回`None`。

Finds the two intersection points of two circles and returns `Dot`. Returns `None` if there are no intersections.

```python
def LineCircleInt(line, circle):
```

寻找一条线和一个圆的一个或两个交点并返回`Dot`，如果没有交点会返回`None`。

Finds one or two intersection points between a line and a circle and returns `Dot`. Returns `None` if there are no intersections.

```python
def LineInt(line1: Line, line2: Line) -> Optional[Tuple[float, float]]:
```

寻找两条线的一个交点并返回`Dot`，如果没有交点会返回`None`。

Finds the intersection point of two lines and returns `Dot`. Returns `None` if there are no intersections.

### 动画 Animations

```python
def VisDrawArc(scene: Scene, p1, p2, angle=PI, axis=OUT):
```

 创建可视化的绘弧动画。显示圆心、半径等，返回绘制的`Arc`，便于之后动画的使用。`scene`，动画场景。`p1`， 代表圆规的针，绘制时不动的点，`numpy.ndarray`类型，即`Dot(...).get_center`得到的结果。`p2`，代表圆规的笔芯，绘制圆弧的点，与`p1`类型相同。`angle`，绘制圆弧的角度，默认`PI`，相当于绘制半个圆。`axis`，只有2个值`IN`和`OUT`，分别表示顺时针还是逆时针作弧。

Creates a visual arc drawing animation. Displays the center, radius, etc., and returns the drawn `Arc` for use in subsequent animations. `scene` is the animation scene. `p1` represents the pivot point of the compass (the fixed point during drawing), of type `numpy.ndarray` (obtained via `Dot(...).get_center`). `p2` represents the pencil point of the compass (the moving point), of the same type as `p1`. `angle` is the angle of the arc to draw (default is `PI`, which draws a semicircle). `axis` can be either `IN` or `OUT`, indicating clockwise or counterclockwise arc drawing, respectively.

---

## 排序工具 Sorting Tool

```python
def sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> None:

# 示例代码 Example code
numbers = [-5, 3, -2, 1, 4]
"""
使用内置的abs函数作为key，即以绝对值大小排序。
Use the built-in abs function as the key to sort by absolute value.
"""
sort(numbers, key=abs)
print(numbers)
# 输出 Output
[1, -2, 3, 4, -5]
```

内省排序`Introsort`，结合了多种排序算法的优点，以确保在各种情况下都能获得高效的性能，不返回列表。`arr`，待排序的列表。`key`，用于比较的键函数，自定义排序规则，而不必修改原始数据。`reverse`，是否降序排列，默认为升序。

Introsort, which combines the advantages of multiple sorting algorithms to ensure efficient performance in all cases. Does not return a list. `arr` is the list to be sorted. `key` is a function to extract a comparison key from each element, allowing custom sorting without modifying the original data. `reverse` specifies whether to sort in descending order (default is ascending).
