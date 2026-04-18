package engine

import (
	"math"
	"testing"
)

func TestRayInit(t *testing.T) {
	v2d := NewVector2d(10.2, 5.3)
	ray := NewRay(math.Pi * 0.25)

	assertApprox3(t, math.Pi*0.25, ray.Ang(), "ang")
	if ray.DirX() != 1 {
		t.Errorf("dirX: expected 1, got %d", ray.DirX())
	}
	if ray.DirY() != 1 {
		t.Errorf("dirY: expected 1, got %d", ray.DirY())
	}
	assertApproxRel(t, 1.4142, ray.DeltaDistX(), 0.0001, "deltaDistX")
	assertApproxRel(t, 1.4142, ray.DeltaDistY(), 0.0001, "deltaDistY")
	assertApproxAbs(t, 1.1314, ray.GetDistX(v2d), 0.0001, "distX")
	assertApproxAbs(t, 0.9899, ray.GetDistY(v2d), 0.0001, "distY")

	ray.Rot(math.Pi * 0.5)
	assertApprox3(t, math.Pi*0.75, ray.Ang(), "ang after rot")
	if ray.DirX() != -1 {
		t.Errorf("dirX: expected -1, got %d", ray.DirX())
	}
	if ray.DirY() != 1 {
		t.Errorf("dirY: expected 1, got %d", ray.DirY())
	}
	assertApproxRel(t, 1.4142, ray.DeltaDistX(), 0.0001, "deltaDistX 2")
	assertApproxRel(t, 1.4142, ray.DeltaDistY(), 0.0001, "deltaDistY 2")
	assertApproxAbs(t, 0.28284, ray.GetDistX(v2d), 0.0001, "distX 2")
	assertApproxAbs(t, 0.9899, ray.GetDistY(v2d), 0.0001, "distY 2")

	ray.Rot(math.Pi * 0.5)
	assertApprox3(t, math.Pi*1.25, ray.Ang(), "ang 3")
	if ray.DirX() != -1 {
		t.Errorf("dirX: expected -1, got %d", ray.DirX())
	}
	if ray.DirY() != -1 {
		t.Errorf("dirY: expected -1, got %d", ray.DirY())
	}
	assertApproxAbs(t, 0.28284, ray.GetDistX(v2d), 0.0001, "distX 3")
	assertApproxAbs(t, 0.42426, ray.GetDistY(v2d), 0.0001, "distY 3")

	ray.Rot(math.Pi * 0.5)
	assertApprox3(t, math.Pi*1.75, ray.Ang(), "ang 4")
	if ray.DirX() != 1 {
		t.Errorf("dirX: expected 1, got %d", ray.DirX())
	}
	if ray.DirY() != -1 {
		t.Errorf("dirY: expected -1, got %d", ray.DirY())
	}
	assertApproxAbs(t, 1.1314, ray.GetDistX(v2d), 0.0001, "distX 4")
	assertApproxAbs(t, 0.42426, ray.GetDistY(v2d), 0.0001, "distY 4")
}

func TestRayCastWall1(t *testing.T) {
	pos := NewVector2d(1.3, 2.2)
	ray := NewRay(math.Pi / 6)

	wall1 := NewWall(2, 3, 10)
	ray.CastWall(pos, NewItemGrid([]Blocker{wall1}))
	if ray.TypeID() == nil || *ray.TypeID() != wall1.TypeID() {
		t.Errorf("typeID: expected %d, got %v", wall1.TypeID(), ray.TypeID())
	}
	if ray.IsVertical() {
		t.Error("should not be vertical")
	}
	if ray.IsInverted() {
		t.Error("should not be inverted")
	}
	assertApproxAbs(t, 2.69, ray.CollidedVector2d().X(), 0.01, "collided x")
	assertApproxAbs(t, 3, ray.CollidedVector2d().Y(), 0.01, "collided y")
	assertApproxAbs(t, 1.39, ray.DistAdjusted(), 0.01, "distAdjusted")
	assertApproxAbs(t, 0.69, ray.Offset(), 0.01, "offset")

	wall2 := NewWall(7, 6, 20)
	ray.CastWall(pos, NewItemGrid([]Blocker{wall2}))
	if ray.TypeID() == nil || *ray.TypeID() != wall2.TypeID() {
		t.Errorf("typeID: expected %d", wall2.TypeID())
	}
	assertApproxAbs(t, 7.88, ray.CollidedVector2d().X(), 0.01, "collided x 2")
	assertApproxAbs(t, 6, ray.CollidedVector2d().Y(), 0.01, "collided y 2")
	assertApproxAbs(t, 6.58, ray.DistAdjusted(), 0.01, "distAdjusted 2")
	assertApproxAbs(t, 0.88, ray.Offset(), 0.01, "offset 2")
}

func TestRayCastWall2(t *testing.T) {
	pos := NewVector2d(4.4, 2.4)
	ray := NewRay(math.Pi + math.Pi/6)

	wall := NewWall(10, 10, 10)
	wall1 := NewWall(3, 1, 10)

	ray.CastWall(pos, NewItemGrid([]Blocker{wall1, wall}))
	if ray.TypeID() == nil || *ray.TypeID() != wall1.TypeID() {
		t.Errorf("typeID: expected %d", wall1.TypeID())
	}
	if ray.IsVertical() {
		t.Error("should not be vertical")
	}
	if !ray.IsInverted() {
		t.Error("should be inverted")
	}
	assertApproxAbs(t, 3.71, ray.CollidedVector2d().X(), 0.01, "collided x")
	assertApproxAbs(t, 2, ray.CollidedVector2d().Y(), 0.01, "collided y")
	assertApproxAbs(t, 0.69, ray.DistAdjusted(), 0.01, "distAdjusted")
	assertApproxAbs(t, 0.71, ray.Offset(), 0.01, "offset")

	wall2 := NewWall(1, 0, 10)
	ray.CastWall(pos, NewItemGrid([]Blocker{wall2, wall}))
	assertApproxAbs(t, 1.98, ray.CollidedVector2d().X(), 0.01, "collided x 2")
	assertApproxAbs(t, 1, ray.CollidedVector2d().Y(), 0.01, "collided y 2")
	assertApproxAbs(t, 2.42, ray.DistAdjusted(), 0.01, "distAdjusted 2")
	assertApproxAbs(t, 0.98, ray.Offset(), 0.01, "offset 2")
}

func TestRayCastWall3(t *testing.T) {
	pos := NewVector2d(1.4, 2.5)
	ray := NewRay(math.Pi / 6)

	wall := NewWall(10, 10, 10)
	wall1 := NewWall(2, 2, 10)

	ray.CastWall(pos, NewItemGrid([]Blocker{wall1, wall}))
	if ray.TypeID() == nil || *ray.TypeID() != wall1.TypeID() {
		t.Errorf("typeID: expected %d", wall1.TypeID())
	}
	if !ray.IsVertical() {
		t.Error("should be vertical")
	}
	if ray.IsInverted() {
		t.Error("should not be inverted")
	}
	assertApproxAbs(t, 2, ray.CollidedVector2d().X(), 0.01, "collided x")
	assertApproxAbs(t, 2.85, ray.CollidedVector2d().Y(), 0.01, "collided y")
	assertApproxAbs(t, 0.6, ray.DistAdjusted(), 0.01, "distAdjusted")
	assertApproxAbs(t, 0.85, ray.Offset(), 0.01, "offset")
}

func TestRayCastDoor1(t *testing.T) {
	pos := NewVector2d(2, 5)
	ray := NewRay(0)
	wall := NewWall(10, 5, 99)
	door1 := NewDoor(5, 2, 1, true)
	door2 := NewDoor(5, 5, 1, true)

	ray.CastWall(pos, NewItemGrid([]Blocker{wall}))
	if ray.TypeID() == nil || *ray.TypeID() != wall.TypeID() {
		t.Errorf("typeID after cast_wall: expected %d", wall.TypeID())
	}

	ray.CastDoors(pos, []*Door{door1, door2})
	if len(ray.Doors()) != 1 {
		t.Errorf("expected 1 door, got %d", len(ray.Doors()))
	}
	assertApproxAbs(t, 3, ray.Doors()[0].Dist(), 0.001, "door dist")
}

func TestRayCastDoor2(t *testing.T) {
	pos := NewVector2d(2, 5)
	ray := NewRay(math.Pi)
	wall := NewWall(0, 5, 99)
	door1 := NewDoor(1, 2, 1, true)
	door2 := NewDoor(1, 5, 1, true)

	ray.CastWall(pos, NewItemGrid([]Blocker{wall}))
	if ray.TypeID() == nil || *ray.TypeID() != wall.TypeID() {
		t.Errorf("typeID after cast_wall: expected %d", wall.TypeID())
	}

	ray.CastDoors(pos, []*Door{door1, door2})
	if len(ray.Doors()) != 1 {
		t.Errorf("expected 1 door, got %d", len(ray.Doors()))
	}
	assertApproxAbs(t, -1, ray.Doors()[0].Dist(), 0.001, "door dist")
}

// helpers used by ray tests

func assertApproxRel(t *testing.T, expected, actual, tol float64, label string) {
	t.Helper()
	if math.Abs(expected-actual)/math.Abs(expected) > tol {
		t.Errorf("%s: expected ~%v, got %v (rel tol %v)", label, expected, actual, tol)
	}
}

func assertApproxAbs(t *testing.T, expected, actual, tol float64, label string) {
	t.Helper()
	if math.Abs(expected-actual) > tol {
		t.Errorf("%s: expected %v ± %v, got %v", label, expected, tol, actual)
	}
}
