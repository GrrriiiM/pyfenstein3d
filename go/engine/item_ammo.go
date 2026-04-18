package engine

// ItemAmmo is a pickup that adds ammo to the player.
type ItemAmmo struct {
	Item
}

// NewItemAmmo creates a new ItemAmmo at the given position.
func NewItemAmmo(x, y float64, typeID int) *ItemAmmo {
	return &ItemAmmo{Item: Item{block: newBlock(x, y, typeID, false, false)}}
}

// Touch adds ammo to the player and removes this item from the grid.
func (ia *ItemAmmo) Touch(player *Player, grid *ItemGrid) {
	player.AddAmmo(4)
	grid.RemoveBlock(ia.X(), ia.Y())
}
