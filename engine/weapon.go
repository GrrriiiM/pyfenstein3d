package engine

// Weapon is a player weapon with a shoot animation.
type Weapon struct {
	typeID         int
	shootInterval  float64
	shootAnimation *Animation
	IsShooting     bool
}

// NewWeapon creates a new Weapon with the given type and shoot interval.
func NewWeapon(typeID int, shootInterval float64) *Weapon {
	w := &Weapon{
		typeID:        typeID,
		shootInterval: shootInterval,
	}
	w.shootAnimation = NewAnimation(0.5, nil, nil)
	return w
}

func (w *Weapon) TypeID() int                { return w.typeID }
func (w *Weapon) ShootInterval() float64      { return w.shootInterval }
func (w *Weapon) ShootAnimation() *Animation  { return w.shootAnimation }

// Update advances the weapon's shoot cycle.
func (w *Weapon) Update(deltaTime float64, person Shooter, grid *ItemGrid) {
	if w.IsShooting && (!w.shootAnimation.IsAnimating() || w.shootAnimation.Time() > w.shootInterval) {
		w.shootAnimation.Start(0)
		person.Shoot()
	}
	w.shootAnimation.Update(deltaTime)
}

// Shooter is the interface required by Weapon.Update.
type Shooter interface {
	Shoot()
}

// WeaponKnife is a melee weapon.
type WeaponKnife struct{ *Weapon }

func NewWeaponKnife() *WeaponKnife { return &WeaponKnife{NewWeapon(120, 0.5)} }

// WeaponPistol is a pistol.
type WeaponPistol struct{ *Weapon }

func NewWeaponPistol() *WeaponPistol { return &WeaponPistol{NewWeapon(121, 0.5)} }

// WeaponSubmachine is a submachine gun.
type WeaponSubmachine struct{ *Weapon }

func NewWeaponSubmachine() *WeaponSubmachine { return &WeaponSubmachine{NewWeapon(122, 0.3)} }

// WeaponMinigun is a minigun.
type WeaponMinigun struct{ *Weapon }

func NewWeaponMinigun() *WeaponMinigun { return &WeaponMinigun{NewWeapon(123, 0.1)} }
