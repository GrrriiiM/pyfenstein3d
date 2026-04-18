package engine

import (
	"math"
	"testing"
)

func TestVector2dInit(t *testing.T) {
	v := NewVector2d(10, 0)
	assertApprox(t, 10, v.X(), "x")
	assertApprox(t, 0, v.Y(), "y")
	assertApprox3(t, 0, v.Ang(), "ang")
	assertApprox3(t, 10, v.Mag(), "mag")

	v2 := NewVector2d(10, 10)
	assertApprox(t, 10, v2.X(), "x2")
	assertApprox(t, 10, v2.Y(), "y2")
	assertApprox3(t, math.Pi/4, v2.Ang(), "ang2")
	assertApprox3(t, 14.142, v2.Mag(), "mag2")
}

func TestVector2dAdd(t *testing.T) {
	v1 := NewVector2d(1, 2)
	v2 := NewVector2d(3, 4)
	v3 := v1.Add(v2)
	assertApprox(t, 4, v3.X(), "x")
	assertApprox(t, 6, v3.Y(), "y")
}

func TestVector2dSub(t *testing.T) {
	v1 := NewVector2d(1, 2)
	v2 := NewVector2d(3, 5)
	v3 := v1.Sub(v2)
	assertApprox(t, -2, v3.X(), "x")
	assertApprox(t, -3, v3.Y(), "y")
}

func TestVector2dMul(t *testing.T) {
	v := NewVector2d(4, 3)
	v = v.Mul(2)
	assertApprox(t, 8, v.X(), "x")
	assertApprox(t, 6, v.Y(), "y")
}

func TestVector2dDiv(t *testing.T) {
	v := NewVector2d(4, 3)
	v = v.Div(2)
	assertApprox(t, 2, v.X(), "x")
	assertApprox(t, 1.5, v.Y(), "y")
}

func TestVector2dFloorDiv(t *testing.T) {
	v := NewVector2d(5, 7)
	v = v.FloorDiv(2)
	assertApprox(t, 2, v.X(), "x")
	assertApprox(t, 3, v.Y(), "y")
}

func TestVector2dRot(t *testing.T) {
	v := NewVector2d(4, 3)
	v = v.Rot(math.Pi / 2)
	assertRound(t, -3, v.X(), "x")
	assertRound(t, 4, v.Y(), "y")
}

func TestVector2dCopy(t *testing.T) {
	v := NewVector2d(4, 3)
	v1 := v.Copy()
	if v == v1 {
		t.Error("copy should be a different pointer")
	}
	assertApprox(t, v.X(), v1.X(), "x")
	assertApprox(t, v.Y(), v1.Y(), "y")
}

func TestVector2dNorm(t *testing.T) {
	v := NewVector2d(4, 3)
	v = v.Norm(1)
	assertApprox(t, 1, v.Mag(), "mag")
}

// helpers

func assertApprox(t *testing.T, expected, actual float64, label string) {
	t.Helper()
	if math.Abs(expected-actual) > 1e-9 {
		t.Errorf("%s: expected %v, got %v", label, expected, actual)
	}
}

func assertApprox3(t *testing.T, expected, actual float64, label string) {
	t.Helper()
	if math.Abs(expected-actual) > 1e-3 {
		t.Errorf("%s: expected %.5f, got %.5f", label, expected, actual)
	}
}

func assertRound(t *testing.T, expected, actual float64, label string) {
	t.Helper()
	if math.Round(actual) != expected {
		t.Errorf("%s: expected round(%v)=%v, got %v", label, actual, expected, math.Round(actual))
	}
}
