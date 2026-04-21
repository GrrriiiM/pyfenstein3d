package engine

// Wall is a solid non-moveable block.
type Wall struct {
	block
}

// NewWall creates a new Wall at the given integer grid position.
func NewWall(x, y float64, typeID int) *Wall {
	return &Wall{block: newBlock(x, y, typeID, true, false)}
}

func (w *Wall) GetBounds(fovAng float64) []*Vector2d {
	// Walls are not filtered via is_in_fov; return empty bounds.
	return nil
}

func (w *Wall) IsInFov(pos *Vector2d, fovAng, fovDelta, dist float64) bool {
	return false
}
