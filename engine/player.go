package engine

// Player is a human-controlled person.
type Player struct {
	*Person
	playerID    string
	health      int
	ammo        int
	score       int
	weaponType  func() *Weapon
}

// NewPlayer creates a new Player at the given position.
func NewPlayer(x, y float64, typeID int, fov *FieldOfView, playerID string) *Player {
	p := &Player{
		Person:   NewPerson(x, y, typeID, fov),
		playerID: playerID,
		health:   100,
		ammo:     8,
	}
	p.ChangeWeapon(NewWeaponPistol)
	return p
}

// CreatePlayer creates a Player using the default factory settings.
func CreatePlayer(x, y float64, typeID int) *Player {
	return NewPlayer(x, y, typeID, NewFieldOfView(0), "123")
}

func (p *Player) Health() int   { return p.health }
func (p *Player) Ammo() int     { return p.ammo }
func (p *Player) Score() int    { return p.score }
func (p *Player) PlayerID() string { return p.playerID }

// Shoot decrements ammo and switches to knife when out.
func (p *Player) Shoot() {
	p.ammo--
	if p.ammo < 0 {
		p.ammo = 0
	}
	if p.ammo <= 0 {
		p.weapon = NewWeaponKnife().Weapon
	}
}

// ChangeWeapon sets the player's weapon type and equips it if ammo > 0.
func (p *Player) ChangeWeapon(factory func() *WeaponPistol) {
	p.weaponType = func() *Weapon { return factory().Weapon }
	if p.ammo > 0 {
		p.weapon = p.weaponType()
	}
}

// ChangeWeaponSubmachine equips a submachine gun.
func (p *Player) ChangeWeaponSubmachine() {
	p.weaponType = func() *Weapon { return NewWeaponSubmachine().Weapon }
	if p.ammo > 0 {
		p.weapon = p.weaponType()
	}
}

// ChangeWeaponMinigun equips a minigun.
func (p *Player) ChangeWeaponMinigun() {
	p.weaponType = func() *Weapon { return NewWeaponMinigun().Weapon }
	if p.ammo > 0 {
		p.weapon = p.weaponType()
	}
}

// AddAmmo increases ammo and re-equips the stored weapon if previously empty.
func (p *Player) AddAmmo(quantity int) {
	p.ammo += quantity
	if p.ammo > 999 {
		p.ammo = 999
	}
	if p.ammo > 0 && p.weaponType != nil {
		p.weapon = p.weaponType()
	}
}

// AddScore increases the player's score.
func (p *Player) AddScore(quantity int) {
	p.score += quantity
}

// Update advances the player, handles item pickup.
func (p *Player) Update(deltaTime float64, grid *ItemGrid) {
	p.Person.Update(deltaTime, grid)
	if grid != nil {
		block := grid.GetBlock(int(p.X()), int(p.Y()))
		if block != nil {
			if t, ok := block.(ItemLike); ok {
				t.Touch(p, grid)
			}
		}
	}
}

// Cast overrides Person.Cast using the actual Player pointer.
func (p *Player) Cast(grid *ItemGrid) {
	p.fov.Cast(p, grid)
}
