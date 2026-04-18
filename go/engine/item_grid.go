package engine

import "math"

// ItemGrid is a 2D spatial grid of blocks.
type ItemGrid struct {
	grid    [][]Blocker
	items   []Blocker
	doors   []*Door
	enemies []*Enemy
	maxX    int
	maxY    int
}

// NewItemGrid creates a new ItemGrid from a list of blocks.
func NewItemGrid(blocks []Blocker) *ItemGrid {
	maxX, maxY := 0, 0
	for _, b := range blocks {
		if b.BlockX() > maxX {
			maxX = b.BlockX()
		}
		if b.BlockY() > maxY {
			maxY = b.BlockY()
		}
	}
	maxX++
	maxY++

	grid := make([][]Blocker, maxX)
	for i := range grid {
		grid[i] = make([]Blocker, maxY)
	}

	ig := &ItemGrid{grid: grid, maxX: maxX, maxY: maxY}

	for _, b := range blocks {
		if _, ok := b.(ItemLike); ok {
			ig.items = append(ig.items, b)
		}
		if door, ok := b.(*Door); ok {
			ig.doors = append(ig.doors, door)
		}
		if enemy, ok := b.(*Enemy); ok {
			ig.enemies = append(ig.enemies, enemy)
		}
		if !b.IsMoveable() {
			ig.grid[b.BlockX()][b.BlockY()] = b
		}
	}
	return ig
}

func (ig *ItemGrid) MaxX() int { return ig.maxX }
func (ig *ItemGrid) MaxY() int { return ig.maxY }

// GetBlock returns the block at the given grid coordinates, or nil if out of bounds.
func (ig *ItemGrid) GetBlock(blockX, blockY int) Blocker {
	bx := int(math.Floor(float64(blockX)))
	by := int(math.Floor(float64(blockY)))
	if bx < ig.maxX && by < ig.maxY && bx >= 0 && by >= 0 {
		return ig.grid[bx][by]
	}
	return nil
}

// RemoveBlock removes the block at the given grid coordinates.
func (ig *ItemGrid) RemoveBlock(x, y float64) {
	bx := int(math.Floor(x))
	by := int(math.Floor(y))
	if bx < ig.maxX && by < ig.maxY && bx >= 0 && by >= 0 {
		ig.grid[bx][by] = nil
	}
}

// GetDoorsByFov returns doors within the field of view.
func (ig *ItemGrid) GetDoorsByFov(pos *Vector2d, fovAng, fovDelta, dist float64) []*Door {
	var result []*Door
	for _, door := range ig.doors {
		if door.IsInFov(pos, fovAng, fovDelta, dist) {
			result = append(result, door)
		}
	}
	return result
}

// GetItemsByFov returns items and enemies within the field of view.
func (ig *ItemGrid) GetItemsByFov(pos *Vector2d, fovAng, fovDelta, dist float64) []Blocker {
	result := ig.getItemsFromGridByFov(pos, fovAng, fovDelta, dist)
	result = append(result, ig.getEnemiesByFov(pos, fovAng, fovDelta, dist)...)
	return result
}

func (ig *ItemGrid) getItemsFromGridByFov(pos *Vector2d, fovAng, fovDelta, dist float64) []Blocker {
	fovAngVecMin := CreateWithAng(fovAng - fovDelta*0.5)
	fovAngVecMax := CreateWithAng(fovAng + fovDelta*0.5)

	startX, endX := 0, ig.maxX
	startY, endY := 0, ig.maxY

	if fovAngVecMin.X() > 0 && fovAngVecMax.X() > 0 {
		startX = int(math.Floor(pos.X()))
	} else if fovAngVecMin.X() < 0 && fovAngVecMax.X() < 0 {
		endX = int(math.Floor(pos.X() + 1))
	}
	if fovAngVecMin.Y() > 0 && fovAngVecMax.Y() > 0 {
		startY = int(math.Floor(pos.Y()))
	} else if fovAngVecMin.Y() < 0 && fovAngVecMax.Y() < 0 {
		endY = int(math.Floor(pos.Y() + 1))
	}

	if startX < 0 {
		startX = 0
	}
	if endX > ig.maxX {
		endX = ig.maxX
	}
	if startY < 0 {
		startY = 0
	}
	if endY > ig.maxY {
		endY = ig.maxY
	}

	var result []Blocker
	for x := startX; x < endX; x++ {
		for y := startY; y < endY; y++ {
			b := ig.grid[x][y]
			if b == nil {
				continue
			}
			if _, ok := b.(ItemLike); !ok {
				continue
			}
			if b.IsInFov(pos, fovAng, fovDelta, dist) {
				result = append(result, b)
			}
		}
	}
	return result
}

func (ig *ItemGrid) getEnemiesByFov(pos *Vector2d, fovAng, fovDelta, dist float64) []Blocker {
	var result []Blocker
	for _, e := range ig.enemies {
		if e.IsInFov(pos, fovAng, fovDelta, dist) {
			result = append(result, e)
		}
	}
	return result
}
