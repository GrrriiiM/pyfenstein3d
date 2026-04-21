package engine

// ItemWeapon is a pickup that changes the player's weapon.
type ItemWeapon struct {
	Item
}

// NewItemWeapon creates a new ItemWeapon at the given position.
func NewItemWeapon(x, y float64, typeID int) *ItemWeapon {
	return &ItemWeapon{Item: Item{block: newBlock(x, y, typeID, false, false)}}
}

// Touch gives the player the corresponding weapon and removes this item.
func (iw *ItemWeapon) Touch(player *Player, grid *ItemGrid) {
	if iw.TypeID() == 85 {
		player.ChangeWeaponSubmachine()
	} else if iw.TypeID() == 86 {
		player.ChangeWeaponMinigun()
	}
	grid.RemoveBlock(iw.X(), iw.Y())
}
