package engine

import "math"

// Enemy is an AI-controlled person.
type Enemy struct {
	*Person
}

// NewEnemy creates a new Enemy at the given position.
func NewEnemy(x, y float64, typeID int, fov *FieldOfView) *Enemy {
	return &Enemy{Person: NewPerson(x, y, typeID, fov)}
}

// CreateEnemy creates the appropriate enemy subtype based on typeID.
func CreateEnemy(x, y float64, typeID int) *Enemy {
	if typeID == 131 {
		return NewEnemyDog(x, y, NewFieldOfView(0)).Enemy
	}
	return NewEnemyGuard(x, y, NewFieldOfView(0)).Enemy
}

func (e *Enemy) GetBounds(fovAng float64) []*Vector2d {
	pos := e.pos.Rot(-fovAng)
	return []*Vector2d{
		NewVector2d(pos.X()-0.5, pos.Y()).Rot(fovAng),
		NewVector2d(pos.X()+0.5, pos.Y()).Rot(fovAng),
	}
}

func (e *Enemy) IsInFov(pos *Vector2d, fovAng, fovDelta, dist float64) bool {
	return blockIsInFov(e.GetBounds(fovAng), pos, fovAng, fovDelta, dist)
}

// GetState returns the directional animation state relative to the player.
func (e *Enemy) GetState(player *Player) int {
	ang := NewVector2d(player.X(), player.Y()).Sub(NewVector2d(e.X(), e.Y())).Ang() + math.Pi
	ang = math.Mod(ang-(e.FovAng()+math.Pi)+math.Pi*2, math.Pi*2)
	interval := math.Pi / 4
	for s := 0; s < 8; s++ {
		if ang < float64(s+1)*interval-interval*0.5 {
			return s
		}
	}
	return 0
}

// EnemyGuard is a human guard enemy.
type EnemyGuard struct{ *Enemy }

func NewEnemyGuard(x, y float64, fov *FieldOfView) *EnemyGuard {
	return &EnemyGuard{Enemy: NewEnemy(x, y, 130, fov)}
}

// EnemyDog is a dog enemy.
type EnemyDog struct{ *Enemy }

func NewEnemyDog(x, y float64, fov *FieldOfView) *EnemyDog {
	return &EnemyDog{Enemy: NewEnemy(x, y, 131, fov)}
}
