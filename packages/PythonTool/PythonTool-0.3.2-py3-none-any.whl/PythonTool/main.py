from manim import *
import math
from typing import *
import heapq

# ManimTool -------------------------------------------------------------------------------------------------------------------------------------------
def ChineseMathTex(*texts, font="SimSun", tex_to_color_map={}, **kwargs):
	tex_template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
	tex_template.add_to_preamble(r"\usepackage{amsmath}")
	tex_template.add_to_preamble(r"\usepackage{xeCJK}")
	tex_template.add_to_preamble(rf"\setCJKmainfont{{{font}}}")

	combined_chinesetext = []
	for text in texts:
		chinesetext = ""
		for i in range(len(text)):
			if ('\u4e00' <= text[i] <= '\u9fff') or ('\u3000' <= text[i] <= '\u303f') or ('\uff00' <= text[i] <= '\uffef'):
				chinesetext += rf"\text{{{text[i]}}}"
			else:
				chinesetext += text[i]
		combined_chinesetext.append(chinesetext)

	new_dict = {}
	for key in tex_to_color_map.keys():
		new_key = ""
		for char in key:
			if ('\u4e00' <= char <= '\u9fff') or ('\u3000' <= char <= '\u303f') or ('\uff00' <= char <= '\uffef'):
				new_key += rf"\text{{{char}}}"
			else:
				new_key += char
		new_dict[new_key] = tex_to_color_map[key]

	return MathTex(*combined_chinesetext, tex_template=tex_template, tex_to_color_map=new_dict, **kwargs)

def YellowLine(**kwargs):
	line = Line(**kwargs).set_color(YELLOW)
	return line

def LabelDot(dot_label, dot_pos, label_pos=DOWN, buff=0.1):
	dot = Dot().move_to(dot_pos)
	label = MathTex(dot_label).next_to(dot, label_pos, buff=buff)
	return VGroup(label, dot)

def MathTexLine(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
	line = Line(**kwargs)
	tex = mathtex.next_to(line, direction, buff=buff)
	return VGroup(tex, line)

def MathTexBrace(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
	brace = Brace(direction=direction, **kwargs)
	tex = mathtex.next_to(brace, direction, buff=buff)
	return VGroup(tex, brace)

def MathTexDoublearrow(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
	doublearrow = DoubleArrow(**kwargs)
	tex = mathtex.next_to(doublearrow, direction, buff=buff)
	return VGroup(tex, doublearrow)

def CircleInt(circle1, circle2):
	circle1_center = circle1.get_center()
	circle1_radius = circle1.radius
	circle2_center = circle2.get_center()
	circle2_radius = circle2.radius
	x1, y1, _ = circle1_center
	x2, y2, _ = circle2_center
	d = math.sqrt((x2 - x1) ** 2+(y2 - y1) ** 2)
	if d > circle1_radius + circle2_radius or d < abs(circle1_radius - circle2_radius):
		return None
	a = (circle1_radius ** 2 - circle2_radius ** 2 + d ** 2)/(2 * d)
	h = math.sqrt(circle1_radius ** 2 - a ** 2)
	xm = x1 + a * (x2 - x1)/d
	ym = y1 + a * (y2 - y1)/d
	xs1 = xm + h * (y2 - y1)/d
	xs2 = xm - h * (y2 - y1)/d
	ys1 = ym - h * (x2 - x1)/d
	ys2 = ym + h * (x2 - x1)/d
	return Dot([xs1, ys1, 0]), Dot([xs2, ys2, 0])

def LineCircleInt(line, circle):
	p1 = line.get_start()
	p2 = line.get_end()
	c = circle.get_center()
	r = circle.radius
	dx, dy, _ = p2 - p1
	cx, cy, _ = p1 - c
	a = dx**2 + dy**2
	b = 2 * (dx * cx + dy * cy)
	c = cx**2 + cy**2 - r**2
	discriminant = b**2 - 4 * a * c
	if discriminant < 0:
		return None
	t1 = (-b + math.sqrt(discriminant)) / (2 * a)
	t2 = (-b - math.sqrt(discriminant)) / (2 * a)
	intersections = []
	for t in [t1, t2]:
		if 0 <= t <= 1:
			intersection = Dot(p1 + t * (p2 - p1))
			intersections.append(intersection)
	return intersections

def LineInt(line1: Line, line2: Line) -> Optional[Tuple[float, float]]:
	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]
	p1 = line1.get_start()[:2]
	p2 = line1.get_end()[:2]
	p3 = line2.get_start()[:2]
	p4 = line2.get_end()[:2]
	xdiff = (p1[0] - p2[0], p3[0] - p4[0])
	ydiff = (p1[1] - p2[1], p3[1] - p4[1])
	div = det(xdiff, ydiff)
	if div == 0:
		return None
	d = (det(p1, p2), det(p3, p4))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div
	return Dot([x, y, 0])

def ExtendedLine(line: Line, extend_distance: float) -> Line:
	start_point = line.get_start()
	end_point = line.get_end()
	direction_vector = end_point - start_point
	unit_direction_vector = direction_vector / np.linalg.norm(direction_vector)
	new_start_point = start_point - extend_distance * unit_direction_vector
	new_end_point = end_point + extend_distance * unit_direction_vector
	extended_line = line.copy().put_start_and_end_on(new_start_point, new_end_point)
	return extended_line

def VisDrawArc(scene: Scene, p1, p2, angle=PI, axis=OUT):
    d1 = Dot(point=p1)
    d2 = Dot(point=p2)
    dl = DashedLine(d1.get_center(), d2.get_center())
    r = np.linalg.norm(p2 - p1)
    arc = ArcBetweenPoints(p2, p2)
    dl.add_updater(lambda z: z.become(DashedLine(d1.get_center(), d2.get_center())))
    if np.array_equal(axis, OUT):
        arc.add_updater(
            lambda z: z.become(
                ArcBetweenPoints(p2, d2.get_center(), radius=r, stroke_color=YELLOW)
            )
        )
    if np.array_equal(axis, IN):
        arc.add_updater(
            lambda z: z.become(
                ArcBetweenPoints(d2.get_center(), p2, radius=r, stroke_color=YELLOW)
            )
        )
    scene.add(d1, d2, dl, arc)
    scene.play(
        Rotate(
            d2,
            about_point=d1.get_center(),
            axis=axis,
            angle=angle,
            rate_func=linear,
        )
    )
    arc.clear_updaters()
    dl.clear_updaters()
    scene.remove(d1, d2, dl)
    return arc


# SortTool ----------------------------------------------------------------------------------------------------------------------------------------------
def sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> None:
    """使用内省排序对列表进行原地排序"""
    if len(arr) <= 1:
        return  # 已经有序或为空
    
    # 比较函数 - 使用 lambda 避免类型变量问题
    compare = lambda a, b: key(a) > key(b) if reverse else key(a) < key(b)
    
    # 计算最大递归深度
    max_depth = 2 * math.log2(len(arr)) if len(arr) > 0 else 0
    
    # 内省排序主循环
    def introsort(start: int, end: int, depth: float) -> None:
        while start < end:
            # 小规模数据使用插入排序
            if end - start <= 16:
                for i in range(start + 1, end + 1):
                    current = arr[i]
                    j = i - 1
                    while j >= start and compare(current, arr[j]):
                        arr[j + 1] = arr[j]
                        j -= 1
                    arr[j + 1] = current
                return
            
            # 递归深度过大时使用堆排序
            if depth <= 0:
                heap_size = end - start + 1
                
                # 构建堆
                for i in range(heap_size // 2 - 1, -1, -1):
                    heapify(start, heap_size, i)
                
                # 一个个交换元素
                for i in range(heap_size - 1, 0, -1):
                    arr[start], arr[start + i] = arr[start + i], arr[start]
                    heapify(start, i, 0)
                return
            
            # 否则使用快速排序
            mid = (start + end) // 2
            a, b, c = start, mid, end
            
            # 三数取中法
            if compare(arr[b], arr[a]):
                arr[a], arr[b] = arr[b], arr[a]
            if compare(arr[c], arr[b]):
                arr[b], arr[c] = arr[c], arr[b]
            if compare(arr[b], arr[a]):
                arr[a], arr[b] = arr[b], arr[a]
            
            # 将基准值放到开头
            arr[start], arr[mid] = arr[mid], arr[start]
            pivot = arr[start]
            
            # 分区过程
            left = start + 1
            right = end
            
            while True:
                while left <= right and compare(arr[left], pivot):
                    left += 1
                while left <= right and compare(pivot, arr[right]):
                    right -= 1
                if left > right:
                    break
                arr[left], arr[right] = arr[right], arr[left]
                left += 1
                right -= 1
            
            # 将基准值放到正确位置
            arr[start], arr[right] = arr[right], arr[start]
            pivot_index = right
            
            # 尾递归优化
            if pivot_index - start < end - pivot_index:
                introsort(start, pivot_index - 1, depth - 1)
                start = pivot_index + 1
            else:
                introsort(pivot_index + 1, end, depth - 1)
                end = pivot_index - 1
    
    # 堆排序辅助函数
    def heapify(start: int, heap_size: int, i: int) -> None:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < heap_size and compare(arr[start + largest], arr[start + left]):
            largest = left
        
        if right < heap_size and compare(arr[start + largest], arr[start + right]):
            largest = right
        
        if largest != i:
            arr[start + i], arr[start + largest] = arr[start + largest], arr[start + i]
            heapify(start, heap_size, largest)
    
    # 启动内省排序
    introsort(0, len(arr) - 1, max_depth)