package engine

import (
	"math"
	"testing"
)

func TestPersonInit(t *testing.T) {
	origMV := PersonMovementVelocity
	origTV := PersonTurnVelocity
	origFA := FovAngle
	defer func() {
		PersonMovementVelocity = origMV
		PersonTurnVelocity = origTV
		FovAngle = origFA
	}()

	PersonMovementVelocity = 1
	PersonTurnVelocity = math.Pi / 2
	FovAngle = math.Pi / 2

	fov := NewFieldOfView(math.Pi)
	person := NewPerson(1, 2, 10, fov)

	assertApprox(t, 1, person.X(), "x init")
	assertApprox(t, 2, person.Y(), "y init")
	assertApprox3(t, math.Pi, person.FovAng(), "fovAng init")

	person.IsMovingBack = true
	person.Update(1, nil)
	assertApprox3(t, 2, person.X(), "x after back")
	assertApprox3(t, 2, person.Y(), "y after back")
	assertApprox3(t, math.Pi, person.FovAng(), "fovAng after back")

	person.IsMovingRight = true
	person.Update(1, nil)
	assertApprox3(t, 2.5, person.X(), "x after right")
	assertApprox3(t, 1.5, person.Y(), "y after right")
	assertApprox3(t, math.Pi, person.FovAng(), "fovAng after right")

	person.Update(1, nil)
	assertApprox3(t, 3, person.X(), "x after second right")
	assertApprox3(t, 1, person.Y(), "y after second right")
	assertApprox3(t, math.Pi, person.FovAng(), "fovAng after second right")

	person.IsTurningLeft = true
	person.Update(1, nil)
	assertApprox3(t, 2.5, person.X(), "x after turn+move")
	assertApprox3(t, 0.5, person.Y(), "y after turn+move")
	assertApprox3(t, math.Pi/2, person.FovAng(), "fovAng after turn")

	person.IsMovingFront = true
	person.IsMovingRight = false
	person.Update(1, nil)
	assertApprox3(t, 2.5, person.X(), "x front+back cancel")
	assertApprox3(t, 0.5, person.Y(), "y front+back cancel")
	assertApprox3(t, 0, person.FovAng(), "fovAng final")
}
