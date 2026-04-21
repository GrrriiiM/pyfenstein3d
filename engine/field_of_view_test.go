package engine

import (
	"math"
	"testing"
)

func TestFieldOfViewInit(t *testing.T) {
	// Temporarily override globals (equivalent to pytest mocker.patch)
	origRayCount := RayCount
	origFovAngle := FovAngle
	defer func() {
		RayCount = origRayCount
		FovAngle = origFovAngle
	}()

	RayCount = 4
	FovAngle = math.Pi

	fov := NewFieldOfView(0)

	if len(fov.Rays()) != 4 {
		t.Errorf("expected 4 rays, got %d", len(fov.Rays()))
	}
	assertApprox(t, 0, fov.Ang(), "ang")
	assertApprox3(t, math.Pi*1.5, fov.AngMin(), "ang_min")
	assertApprox3(t, math.Pi*0.5, fov.AngMax(), "ang_max")

	fov.Rot(math.Pi / 2)
	assertApprox3(t, math.Pi/2, fov.Ang(), "ang after rot")
	assertApprox3(t, 0, fov.AngMin(), "ang_min after rot")
	assertApprox3(t, math.Pi, fov.AngMax(), "ang_max after rot")
}
