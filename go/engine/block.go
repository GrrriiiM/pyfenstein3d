package engine

import "math"

// Blocker is the common interface for all block types in the engine.
type Blocker interface {
	X() float64
	Y() float64
	BlockX() int
	BlockY() int
	OffsetX() float64
	OffsetY() float64
	TypeID() int
	IsSolid() bool
	IsMoveable() bool
	GetBounds(fovAng float64) []*Vector2d
	IsInFov(pos *Vector2d, fovAng, fovDelta, dist float64) bool
	Interacted()
	GetState(player *Player) int
}

// ItemLike is implemented by Item and all its subclasses (has a Touch method).
type ItemLike interface {
	Blocker
	Touch(player *Player, grid *ItemGrid)
}

// block holds common position and type data for all block types.
type block struct {
	pos        *Vector2d
	typeID     int
	isSolid    bool
	isMoveable bool
	blockX     int
	blockY     int
	offsetX    float64
	offsetY    float64
}

func newBlock(x, y float64, typeID int, isSolid, isMoveable bool) block {
	b := block{
		pos:        NewVector2d(x, y),
		typeID:     typeID,
		isSolid:    isSolid,
		isMoveable: isMoveable,
	}
	b.setXY(x, y)
	return b
}

func (b *block) setXY(x, y float64) {
	b.pos = NewVector2d(x, y)
	b.blockX = int(math.Floor(x))
	b.blockY = int(math.Floor(y))
	b.offsetX = math.Mod(x, 1)
	b.offsetY = math.Mod(y, 1)
}

func (b *block) X() float64      { return b.pos.X() }
func (b *block) Y() float64      { return b.pos.Y() }
func (b *block) BlockX() int     { return b.blockX }
func (b *block) BlockY() int     { return b.blockY }
func (b *block) OffsetX() float64 { return b.offsetX }
func (b *block) OffsetY() float64 { return b.offsetY }
func (b *block) TypeID() int     { return b.typeID }
func (b *block) IsSolid() bool   { return b.isSolid }
func (b *block) IsMoveable() bool { return b.isMoveable }
func (b *block) Interacted()     {}
func (b *block) GetState(player *Player) int { return 0 }

// blockIsInFov is a helper used by all concrete types that implement IsInFov.
func blockIsInFov(bounds []*Vector2d, pos *Vector2d, fovAng, fovDelta, dist float64) bool {
	for _, bound := range bounds {
		boundPos := bound.Sub(pos).Rot(-fovAng)
		if dist > boundPos.Mag() {
			boundAng := boundPos.Ang()
			if boundAng > math.Pi {
				boundAng -= math.Pi * 2
			}
			if -fovDelta*0.5 <= boundAng && boundAng <= fovDelta*0.5 {
				return true
			}
		}
	}
	return false
}
