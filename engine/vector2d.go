package engine

import "math"

// Vector2d represents a 2D vector with precomputed angle and magnitude.
type Vector2d struct {
	x, y, ang, mag float64
}

// NewVector2d creates a Vector2d from x and y components.
func NewVector2d(x, y float64) *Vector2d {
	ang := math.Mod(math.Atan2(y, x)+math.Pi*2, math.Pi*2)
	mag := math.Sqrt(x*x + y*y)
	return &Vector2d{x: x, y: y, ang: ang, mag: mag}
}

// CreateWithAng creates a unit Vector2d from an angle in radians.
func CreateWithAng(rad float64) *Vector2d {
	return NewVector2d(math.Cos(rad), math.Sin(rad))
}

func (v *Vector2d) X() float64   { return v.x }
func (v *Vector2d) Y() float64   { return v.y }
func (v *Vector2d) Ang() float64 { return v.ang }
func (v *Vector2d) Mag() float64 { return v.mag }

// Copy returns a new Vector2d with the same components.
func (v *Vector2d) Copy() *Vector2d { return NewVector2d(v.x, v.y) }

// Add returns v + other.
func (v *Vector2d) Add(other *Vector2d) *Vector2d {
	return NewVector2d(v.x+other.x, v.y+other.y)
}

// Sub returns v - other.
func (v *Vector2d) Sub(other *Vector2d) *Vector2d {
	return NewVector2d(v.x-other.x, v.y-other.y)
}

// Mul returns v * scalar.
func (v *Vector2d) Mul(scalar float64) *Vector2d {
	return NewVector2d(v.x*scalar, v.y*scalar)
}

// Div returns v / scalar.
func (v *Vector2d) Div(scalar float64) *Vector2d {
	return NewVector2d(v.x/scalar, v.y/scalar)
}

// FloorDiv returns floor(v / scalar) component-wise.
func (v *Vector2d) FloorDiv(scalar float64) *Vector2d {
	return NewVector2d(math.Floor(v.x/scalar), math.Floor(v.y/scalar))
}

// Rot rotates v by rad radians and returns the result (equivalent to ** in Python).
func (v *Vector2d) Rot(rad float64) *Vector2d {
	cos := math.Cos(rad)
	sin := math.Sin(rad)
	return NewVector2d(v.x*cos-v.y*sin, v.x*sin+v.y*cos)
}

// Norm returns a vector in the same direction as v with the given magnitude (equivalent to % in Python).
func (v *Vector2d) Norm(mag float64) *Vector2d {
	if v.mag == 0 {
		return v
	}
	return NewVector2d((v.x/v.mag)*mag, (v.y/v.mag)*mag)
}
