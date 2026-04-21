package engine

import (
	"testing"
)

func TestMap2dCreateWithPattern(t *testing.T) {
	pattern := "0B010F110A\n3CFF3E  3C"
	m := CreateWithPattern(pattern)
	grid := m.Grid()

	assertWall := func(x, y, typeID int) {
		t.Helper()
		b := grid.GetBlock(x, y)
		if b == nil {
			t.Fatalf("(%d,%d) is nil, expected Wall typeID=%d", x, y, typeID)
		}
		if _, ok := b.(*Wall); !ok {
			t.Fatalf("(%d,%d) is %T, expected *Wall", x, y, b)
		}
		if b.TypeID() != typeID {
			t.Errorf("(%d,%d) typeID: expected %d, got %d", x, y, typeID, b.TypeID())
		}
	}
	assertDecoration := func(x, y, typeID int, solid bool) {
		t.Helper()
		b := grid.GetBlock(x, y)
		if b == nil {
			t.Fatalf("(%d,%d) is nil, expected Decoration", x, y)
		}
		d, ok := b.(*Decoration)
		if !ok {
			t.Fatalf("(%d,%d) is %T, expected *Decoration", x, y, b)
		}
		if d.TypeID() != typeID {
			t.Errorf("(%d,%d) typeID: expected %d, got %d", x, y, typeID, d.TypeID())
		}
		if d.IsSolid() != solid {
			t.Errorf("(%d,%d) isSolid: expected %v, got %v", x, y, solid, d.IsSolid())
		}
	}

	// Row 0: "0B010F110A" → 0x0B=11, 0x01=1, 0x0F=15, 0x11=17, 0x0A=10
	assertWall(0, 0, 11)
	assertWall(1, 0, 1)
	assertWall(2, 0, 15)
	assertWall(3, 0, 17)
	assertWall(4, 0, 10)

	// Row 1: "3CFF3E  3C" → 0x3C=60(solid decoration), 0xFF=255(player), 0x3E=62(non-solid dec), "  "=skip, 0x3C=60
	assertDecoration(0, 1, 60, true)
	assertDecoration(2, 1, 62, false)
	b := grid.GetBlock(3, 1)
	if b != nil {
		t.Errorf("(3,1) should be nil (spaces), got %T", b)
	}
	assertDecoration(4, 1, 60, true)
}
