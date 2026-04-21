package engine

import (
	"math"
	"testing"
)

func TestItemInit(t *testing.T) {
	item := NewItem(1.5, 3.7, 20, true)
	assertApprox(t, 1.5, item.X(), "x")
	assertApprox(t, 3.7, item.Y(), "y")
	if item.BlockX() != 1 {
		t.Errorf("blockX: expected 1, got %d", item.BlockX())
	}
	if item.BlockY() != 3 {
		t.Errorf("blockY: expected 3, got %d", item.BlockY())
	}
	assertApprox3(t, 0.5, item.OffsetX(), "offsetX")
	assertApprox3(t, math.Mod(3.7, 1), item.OffsetY(), "offsetY")
	if !item.IsSolid() {
		t.Error("expected solid")
	}
}
