package engine

// Item is a non-wall, non-person block that can be interacted with.
type Item struct {
	block
}

// NewItem creates a new Item at the given position.
func NewItem(x, y float64, typeID int, isSolid bool) *Item {
	return &Item{block: newBlock(x, y, typeID, isSolid, false)}
}

func (it *Item) GetBounds(fovAng float64) []*Vector2d {
	pos := it.pos.Rot(-fovAng)
	return []*Vector2d{
		NewVector2d(pos.X()-0.5, pos.Y()).Rot(fovAng),
		NewVector2d(pos.X()+0.5, pos.Y()).Rot(fovAng),
	}
}

func (it *Item) IsInFov(pos *Vector2d, fovAng, fovDelta, dist float64) bool {
	return blockIsInFov(it.GetBounds(fovAng), pos, fovAng, fovDelta, dist)
}

// Touch is a no-op for base Item (overridden by subclasses).
func (it *Item) Touch(player *Player, grid *ItemGrid) {}
