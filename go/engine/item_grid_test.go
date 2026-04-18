package engine

import (
	"testing"
)

func TestItemGridInit(t *testing.T) {
	item := NewItem(0, 0, 10, false)
	decoration := NewDecoration(5, 1, 20, false)
	decorationSolid := NewDecoration(10, 15, 30, true)
	wall := NewWall(2, 23, 40)

	grid := NewItemGrid([]Blocker{item, decoration, decorationSolid, wall})

	if grid.MaxX() != 11 {
		t.Errorf("maxX: expected 11, got %d", grid.MaxX())
	}
	if grid.MaxY() != 24 {
		t.Errorf("maxY: expected 24, got %d", grid.MaxY())
	}
	if grid.GetBlock(0, 0) != item {
		t.Error("block at (0,0) should be item")
	}
	if grid.GetBlock(5, 1) != decoration {
		t.Error("block at (5,1) should be decoration")
	}
	if grid.GetBlock(10, 15) != decorationSolid {
		t.Error("block at (10,15) should be decorationSolid")
	}
	if grid.GetBlock(2, 23) != wall {
		t.Error("block at (2,23) should be wall")
	}
}
