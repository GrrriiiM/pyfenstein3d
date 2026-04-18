package engine

import "math"

// FieldOfView manages a set of rays forming the player's field of view.
type FieldOfView struct {
	vector2dAng    *Vector2d
	vector2dAngMin *Vector2d
	vector2dAngMax *Vector2d
	dist           float64
	rays           []*Ray
}

// NewFieldOfView creates a FieldOfView at the given initial angle,
// using the current RayCount and FovAngle package variables.
func NewFieldOfView(angle float64) *FieldOfView {
	fovAngle := FovAngle
	rayCount := RayCount

	angAbsMin := math.Mod(fovAngle*-0.5+math.Pi*2, math.Pi*2)
	angAbsMax := math.Mod(fovAngle*0.5+math.Pi*2, math.Pi*2)

	fov := &FieldOfView{
		vector2dAng:    NewVector2d(1, 0),
		vector2dAngMin: NewVector2d(1, 0).Rot(angAbsMin),
		vector2dAngMax: NewVector2d(1, 0).Rot(angAbsMax),
	}

	rc := rayCount - rayCount%2
	rayAngle := fovAngle / float64(rayCount-1)
	fov.rays = make([]*Ray, rc)
	for c := 0; c < rc; c++ {
		fov.rays[c] = NewRay(float64(c)*rayAngle - fovAngle/2)
	}

	fov.Rot(angle)
	return fov
}

func (f *FieldOfView) Ang() float64    { return f.vector2dAng.Ang() }
func (f *FieldOfView) AngMin() float64 { return f.vector2dAngMin.Ang() }
func (f *FieldOfView) AngMax() float64 { return f.vector2dAngMax.Ang() }
func (f *FieldOfView) Rays() []*Ray    { return f.rays }

// Rot rotates the entire field of view by rad radians.
func (f *FieldOfView) Rot(rad float64) {
	f.vector2dAng = f.vector2dAng.Rot(rad)
	f.vector2dAngMin = f.vector2dAngMin.Rot(rad)
	f.vector2dAngMax = f.vector2dAngMax.Rot(rad)
	for _, ray := range f.rays {
		ray.Rot(rad)
	}
}

// Cast performs wall, door, and item raycasting from the player's position.
func (f *FieldOfView) Cast(player *Player, grid *ItemGrid) {
	pos := NewVector2d(player.X(), player.Y())

	for _, ray := range f.rays {
		ray.CastWall(pos, grid)
		if ray.Dist() > f.dist {
			f.dist = ray.Dist()
		}
	}

	maxDist := 0.0
	for _, ray := range f.rays {
		if ray.Dist() > maxDist {
			maxDist = ray.Dist()
		}
	}

	doors := grid.GetDoorsByFov(pos, f.Ang(), FovAngle, maxDist)
	for _, ray := range f.rays {
		ray.CastDoors(pos, doors)
		if ray.Dist() > f.dist {
			f.dist = ray.Dist()
		}
	}

	maxDist = 0.0
	for _, ray := range f.rays {
		if ray.Dist() > maxDist {
			maxDist = ray.Dist()
		}
	}

	items := grid.GetItemsByFov(pos, f.Ang(), FovAngle, maxDist)
	for _, ray := range f.rays {
		ray.CastItems(player, items)
	}
}
