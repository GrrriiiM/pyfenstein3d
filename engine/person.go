package engine

import "math"

// Person is the base type for all moving characters (player, enemies).
type Person struct {
	block
	fov            *FieldOfView
	lastPos        *Vector2d
	IsTurningLeft  bool
	IsTurningRight bool
	IsMovingFront  bool
	IsMovingBack   bool
	IsMovingLeft   bool
	IsMovingRight  bool
	IsInteracting  bool
	weapon         *Weapon
}

// NewPerson creates a new Person at the given position with the given FieldOfView.
func NewPerson(x, y float64, typeID int, fov *FieldOfView) *Person {
	p := &Person{
		block:  newBlock(x, y, typeID, true, true),
		fov:    fov,
		weapon: NewWeaponPistol().Weapon,
	}
	p.lastPos = p.pos.Copy()
	return p
}

func (p *Person) Fov() *FieldOfView { return p.fov }
func (p *Person) FovAng() float64   { return p.fov.Ang() }
func (p *Person) Weapon() *Weapon   { return p.weapon }

// GetBounds returns bounding points used for FoV culling.
func (p *Person) GetBounds(fovAng float64) []*Vector2d {
	pos := p.pos.Rot(-fovAng)
	return []*Vector2d{
		NewVector2d(pos.X()-0.5, pos.Y()).Rot(fovAng),
		NewVector2d(pos.X()+0.5, pos.Y()).Rot(fovAng),
	}
}

func (p *Person) IsInFov(pos *Vector2d, fovAng, fovDelta, dist float64) bool {
	return blockIsInFov(p.GetBounds(fovAng), pos, fovAng, fovDelta, dist)
}

// Shoot is a no-op for Person (overridden by Player).
func (p *Person) Shoot() {}

// Update advances the person's movement and weapon state.
func (p *Person) Update(deltaTime float64, grid *ItemGrid) {
	if p.IsTurningLeft {
		p.Turn(-PersonTurnVelocity * deltaTime)
	}
	if p.IsTurningRight {
		p.Turn(PersonTurnVelocity * deltaTime)
	}
	movX, movY := 0.0, 0.0
	count := 0
	if p.IsMovingFront {
		movX += PersonMovementVelocity * deltaTime
		count++
	}
	if p.IsMovingBack {
		movX -= PersonMovementVelocity * deltaTime
		count++
	}
	if p.IsMovingRight {
		movY += PersonMovementVelocity * deltaTime
		count++
	}
	if p.IsMovingLeft {
		movY -= PersonMovementVelocity * deltaTime
		count++
	}
	if movX != 0 || movY != 0 {
		p.Move(NewVector2d(movX/float64(count), movY/float64(count)))
	}
	if p.IsInteracting && grid != nil {
		p.Interact(grid)
	}
	p.weapon.Update(deltaTime, p, grid)
}

// AdjustCollision resolves wall collisions after movement.
func (p *Person) AdjustCollision(grid *ItemGrid) {
	diffPos := p.pos.Sub(p.lastPos)

	bx := int(math.Floor(p.pos.X() + math.Copysign(0.5, diffPos.X())))
	by := int(math.Floor(p.lastPos.Y()))
	item := grid.GetBlock(bx, by)
	if item != nil && item.IsSolid() {
		if diffPos.X() > 0 {
			p.setXY(float64(item.BlockX())-0.5, p.pos.Y())
		} else if diffPos.X() < 0 {
			p.setXY(float64(item.BlockX())+1.5, p.pos.Y())
		}
	}

	bx2 := int(math.Floor(p.lastPos.X()))
	by2 := int(math.Floor(p.pos.Y() + math.Copysign(0.5, diffPos.Y())))
	item2 := grid.GetBlock(bx2, by2)
	if item2 != nil && item2.IsSolid() {
		if diffPos.Y() > 0 {
			p.setXY(p.pos.X(), float64(item2.BlockY())-0.5)
		} else if diffPos.Y() < 0 {
			p.setXY(p.pos.X(), float64(item2.BlockY())+1.5)
		}
	}
}

// Cast performs raycasting for this person.
func (p *Person) Cast(grid *ItemGrid) {
	p.fov.Cast(p.asPlayer(), grid)
}

// Move translates the person in the direction of their facing angle.
func (p *Person) Move(movement *Vector2d) {
	p.lastPos = p.pos.Copy()
	p.pos = p.pos.Rot(-p.fov.Ang()).Add(movement).Rot(p.fov.Ang())
	p.block.setXY(p.pos.X(), p.pos.Y())
}

// Turn rotates the person's field of view by the given angle.
func (p *Person) Turn(angle float64) {
	p.fov.Rot(angle)
}

// Interact attempts to interact with the block the person is facing.
func (p *Person) Interact(grid *ItemGrid) {
	viewDir := CreateWithAng(p.fov.Ang()).Norm(0.75).Add(p.pos)
	block := grid.GetBlock(int(viewDir.X()), int(viewDir.Y()))
	if block != nil {
		block.Interacted()
	}
}

// asPlayer returns a *Player view of this Person (needed for Cast).
// Person directly exposes its block data; we cast via a thin wrapper.
func (p *Person) asPlayer() *Player {
	// This is only called when Person is used standalone (tests);
	// actual Player embeds Person so this is not used in production.
	return &Player{Person: p}
}
