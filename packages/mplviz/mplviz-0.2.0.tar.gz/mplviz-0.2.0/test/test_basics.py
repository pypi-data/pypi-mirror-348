import pytest
import matplotlib.pyplot as plt
import numpy as np
from . import Viz  # Replace with actual module name

@pytest.fixture
def setup_viz():
    fig, ax = plt.subplots()
    return Viz(ax), ax, fig

@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')  

def test_viz_initialization(setup_viz):
    viz, ax, _ = setup_viz
    assert isinstance(viz, Viz)

def test_set_title(setup_viz):
    viz, ax, _ = setup_viz
    viz.set_title("Title")
    assert ax.get_title() == "Title"

def test_xlabel(setup_viz):
    viz, ax, _ = setup_viz
    viz.xlabel("X")
    assert ax.get_xlabel() == "X"

def test_ylabel(setup_viz):
    viz, ax, _ = setup_viz
    viz.ylabel("Y")
    assert ax.get_ylabel() == "Y"

def test_legend(setup_viz):
    viz, ax, _ = setup_viz
    viz.plot([1, 2], [2, 3], label="line").legend()
    assert len(ax.get_legend().get_texts()) == 1


def test_grid(setup_viz):
    viz, ax, _ = setup_viz
    viz.grid(True)
    # Check that gridlines are visible
    assert any(line.get_visible() for line in ax.get_xgridlines())
    assert any(line.get_visible() for line in ax.get_ygridlines())

def test_plot(setup_viz):
    viz, ax, _ = setup_viz
    viz.plot([0, 1], [1, 0])
    assert len(ax.lines) == 1

def test_scatter(setup_viz):
    viz, ax, _ = setup_viz
    viz.scatter([0, 1], [1, 0])
    assert len(ax.collections) == 1

def test_bar(setup_viz):
    viz, ax, _ = setup_viz
    viz.bar([1, 2, 3], [3, 2, 1])
    assert len(ax.patches) == 3

def test_set_xlim(setup_viz):
    viz, ax, _ = setup_viz
    viz.set_xlim(0, 10)
    assert ax.get_xlim() == (0.0, 10.0)

def test_set_ylim(setup_viz):
    viz, ax, _ = setup_viz
    viz.set_ylim(0, 20)
    assert ax.get_ylim() == (0.0, 20.0)

def test_annotate(setup_viz):
    viz, ax, _ = setup_viz
    viz.annotate("point", xy=(1, 1))
    assert len(ax.texts) == 1

def test_figsize(setup_viz):
    viz, _, fig = setup_viz
    viz.figsize((6, 4))
    assert fig.get_size_inches()[0] == 6

def test_tight_layout(setup_viz):
    viz, _, _ = setup_viz
    result = viz.tight_layout()
    assert isinstance(result, Viz)

def test_set_xticks(setup_viz):
    viz, ax, _ = setup_viz
    viz.set_xticks([1, 2, 3])
    assert list(ax.get_xticks())[:3] == [1, 2, 3]

def test_set_yticks(setup_viz):
    viz, ax, _ = setup_viz
    viz.set_yticks([4, 5, 6])
    assert list(ax.get_yticks())[:3] == [4, 5, 6]

def test_invert_x(setup_viz):
    viz, ax, _ = setup_viz
    viz.invert_x()
    assert ax.xaxis_inverted()

def test_invert_y(setup_viz):
    viz, ax, _ = setup_viz
    viz.invert_y()
    assert ax.yaxis_inverted()

def test_hlines(setup_viz):
    viz, ax, _ = setup_viz
    before = len(ax.collections)
    viz.hlines(y=1, xmin=0, xmax=1)
    after = len(ax.collections)
    assert after == before + 1  # One new LineCollection added

def test_vlines(setup_viz):
    viz, ax, _ = setup_viz
    before = len(ax.collections)
    viz.vlines(x=1, ymin=0, ymax=1)
    after = len(ax.collections)
    assert after == before + 1

def test_clear(setup_viz):
    viz, ax, _ = setup_viz
    viz.plot([1], [1])
    viz.clear()
    assert not ax.lines

def test_aspect(setup_viz):
    viz, ax, _ = setup_viz
    viz.aspect('equal')
    assert ax.get_aspect() == 1.0  # 'equal' maps to 1.0 internally


def test_twinx(setup_viz):
    viz, _, _ = setup_viz
    twin = viz.twinx()
    assert isinstance(twin, Viz)

def test_style(setup_viz):
    viz, _, _ = setup_viz
    result = viz.style("ggplot")
    assert isinstance(result, Viz)

def test_imshow(setup_viz):
    viz, ax, _ = setup_viz
    data = np.random.rand(10, 10)
    viz.imshow(data)
    assert len(ax.images) == 1

def test_contour(setup_viz):
    viz, ax, _ = setup_viz
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X**2 + Y**2)
    viz.contour(X, Y, Z)
    assert len(ax.collections) > 0

def test_close(setup_viz):
    viz, _, fig = setup_viz
    viz.close()
    assert not plt.fignum_exists(fig.number)

def test_add_subplot():
    fig = plt.figure()
    viz = Viz(fig.add_subplot(111), fig)
    new_viz = viz.add_subplot(1, 2, 1)
    assert isinstance(new_viz, Viz)

def test_combine_viz():
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    viz1 = Viz(ax1, fig1).plot([1, 2], [3, 4]).set_title("Plot 1")
    viz2 = Viz(ax2, fig2).plot([1, 2], [2, 3]).set_title("Plot 2")
    combined = Viz.combine_viz([viz1, viz2])
    assert isinstance(combined, Viz)
