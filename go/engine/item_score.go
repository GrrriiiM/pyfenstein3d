package engine

// ItemScore is a pickup that adds score to the player.
type ItemScore struct {
	Item
}

// NewItemScore creates a new ItemScore at the given position.
func NewItemScore(x, y float64, typeID int) *ItemScore {
	return &ItemScore{Item: Item{block: newBlock(x, y, typeID, false, false)}}
}

// Touch adds score to the player and removes this item from the grid.
func (is *ItemScore) Touch(player *Player, grid *ItemGrid) {
	switch is.TypeID() {
	case 87:
		player.AddScore(100)
	case 88:
		player.AddScore(400)
	case 89:
		player.AddScore(800)
	}
	grid.RemoveBlock(is.X(), is.Y())
}
