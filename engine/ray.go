package engine

import "math"

// Ray represents a single cast ray in the field of view.
type Ray struct {
	relAng       float64
	vector2dAng  *Vector2d
	vector2d     *Vector2d
	distAdjusted float64
	dist         float64
	offset       float64
	isVertical   bool
	isInverted   bool
	typeID       *int
	dirX         int
	dirY         int
	deltaDistX   float64
	deltaDistY   float64
	items        []*RayItem
	doors        []*RayDoor
}

// NewRay creates a new Ray at the given relative angle.
func NewRay(angle float64) *Ray {
	r := &Ray{
		relAng:      angle,
		vector2dAng: NewVector2d(1, 0),
		vector2d:    NewVector2d(0, 0),
		items:       []*RayItem{},
		doors:       []*RayDoor{},
	}
	r.Rot(angle)
	return r
}

func (r *Ray) Ang() float64          { return r.vector2dAng.Ang() }
func (r *Ray) DirX() int             { return r.dirX }
func (r *Ray) DirY() int             { return r.dirY }
func (r *Ray) DeltaDistX() float64   { return r.deltaDistX }
func (r *Ray) DeltaDistY() float64   { return r.deltaDistY }
func (r *Ray) TypeID() *int          { return r.typeID }
func (r *Ray) Offset() float64       { return r.offset }
func (r *Ray) IsVertical() bool      { return r.isVertical }
func (r *Ray) IsInverted() bool      { return r.isInverted }
func (r *Ray) DistAdjusted() float64 { return r.distAdjusted }
func (r *Ray) Dist() float64         { return r.dist }
func (r *Ray) CollidedVector2d() *Vector2d { return r.vector2d }

func (r *Ray) Items() []*RayItem { return r.items }
func (r *Ray) Doors() []*RayDoor { return r.doors }

// GetDistX returns the distance to the next x-boundary from pos.
func (r *Ray) GetDistX(pos *Vector2d) float64 {
	cosAng := math.Cos(r.Ang())
	if cosAng == 0 {
		return math.Inf(1)
	}
	if r.dirX == 1 {
		return math.Abs((1 - math.Mod(pos.X(), 1)) / cosAng)
	}
	if r.dirX == -1 {
		return math.Abs(math.Mod(pos.X(), 1) / cosAng)
	}
	return math.Inf(1)
}

// GetDistY returns the distance to the next y-boundary from pos.
func (r *Ray) GetDistY(pos *Vector2d) float64 {
	sinAng := math.Sin(r.Ang())
	if sinAng == 0 {
		return math.Inf(1)
	}
	if r.dirY == 1 {
		return math.Abs((1 - math.Mod(pos.Y(), 1)) / sinAng)
	}
	if r.dirY == -1 {
		return math.Abs(math.Mod(pos.Y(), 1) / sinAng)
	}
	return math.Inf(1)
}

// CastWall performs DDA ray-wall intersection against the grid.
func (r *Ray) CastWall(pos *Vector2d, grid *ItemGrid) {
	distX := r.GetDistX(pos)
	distY := r.GetDistY(pos)
	blockX := int(math.Floor(pos.X()))
	blockY := int(math.Floor(pos.Y()))

	for blockX < grid.MaxX() || blockY < grid.MaxY() {
		if distY < distX {
			blockY += r.dirY
			item := grid.GetBlock(blockX, blockY)
			if _, ok := item.(*Wall); ok {
				r.vector2d = NewVector2d(
					math.Cos(r.Ang())*distY,
					math.Sin(r.Ang())*distY,
				).Add(pos)
				r.distAdjusted = math.Abs(math.Cos(r.relAng) * distY)
				r.dist = math.Abs(distY)
				r.isInverted = pos.Y() > item.Y()
				r.offset = math.Mod(r.vector2d.X(), 1)
				r.isVertical = false
				belowOrAbove := blockY + 1
				if r.isInverted {
					belowOrAbove = blockY + 1
				} else {
					belowOrAbove = blockY - 1
				}
				if _, ok2 := grid.GetBlock(blockX, belowOrAbove).(*Door); ok2 {
					tid := 50
					r.typeID = &tid
				} else {
					tid := item.TypeID()
					r.typeID = &tid
				}
				return
			}
			distY += r.deltaDistY
		} else {
			blockX += r.dirX
			item := grid.GetBlock(blockX, blockY)
			if _, ok := item.(*Wall); ok {
				r.vector2d = NewVector2d(
					math.Cos(r.Ang())*distX,
					math.Sin(r.Ang())*distX,
				).Add(pos)
				r.distAdjusted = math.Abs(math.Cos(r.relAng) * distX)
				r.dist = math.Abs(distX)
				r.isInverted = pos.X() > item.X()
				r.offset = math.Mod(r.vector2d.Y(), 1)
				r.isVertical = true
				sideOrOther := blockX + 1
				if r.isInverted {
					sideOrOther = blockX + 1
				} else {
					sideOrOther = blockX - 1
				}
				if _, ok2 := grid.GetBlock(sideOrOther, blockY).(*Door); ok2 {
					tid := 50
					r.typeID = &tid
				} else {
					tid := item.TypeID()
					r.typeID = &tid
				}
				return
			}
			distX += r.deltaDistX
		}
	}
}

// CastDoors checks door intersections for visible doors.
func (r *Ray) CastDoors(pos *Vector2d, doors []*Door) {
	r.doors = []*RayDoor{}
	for _, door := range doors {
		if door.IsVertical() {
			isInverted := r.Ang() >= math.Pi*0.5 && r.Ang() <= math.Pi*1.5
			if !isInverted && door.X() > r.vector2d.X() {
				continue
			}
			if isInverted && door.X() < r.vector2d.X() {
				continue
			}
			x := door.X() - pos.X()
			y := math.Tan(r.Ang()) * x
			v := NewVector2d(x, y)
			posY := pos.Y() + y
			if posY < door.Y() || posY > door.Y()+1 {
				continue
			}
			distAdjusted := math.Sin(math.Pi/2-r.relAng) * v.Mag()
			offset := math.Mod(door.Y()-posY, 1)
			r.doors = append(r.doors, newRayDoor(distAdjusted, offset, door.IsVertical()))
			if v.Mag() < r.dist {
				r.dist = v.Mag()
				r.vector2d = v.Add(pos)
				r.distAdjusted = distAdjusted
			}
		} else {
			isInverted := r.Ang() >= math.Pi && r.Ang() <= math.Pi*2
			if !isInverted && door.Y() > r.vector2d.Y() {
				continue
			}
			if isInverted && door.Y() < r.vector2d.Y() {
				continue
			}
			y := door.Y() - pos.Y()
			x := y / math.Tan(r.Ang())
			v := NewVector2d(x, y)
			posX := pos.X() + x
			if posX < door.X() || posX > door.X()+1 {
				continue
			}
			distAdjusted := math.Sin(math.Pi/2-r.relAng) * v.Mag()
			offset := math.Mod(door.X()-posX, 1)
			r.doors = append(r.doors, newRayDoor(distAdjusted, offset, door.IsVertical()))
			if v.Mag() < r.dist {
				r.dist = v.Mag()
				r.vector2d = v.Add(pos)
				r.distAdjusted = distAdjusted
			}
		}
	}
}

// CastItems checks item/enemy intersections behind the wall hit.
func (r *Ray) CastItems(player *Player, items []Blocker) {
	r.items = []*RayItem{}
	pos := NewVector2d(player.X(), player.Y())
	if r.typeID != nil {
		for _, i := range items {
			itemPos := NewVector2d(i.X(), i.Y()).Sub(pos)
			rayPos := r.vector2d.Sub(pos)
			if itemPos.Mag() < rayPos.Mag() {
				rayPos = rayPos.Rot(-r.Ang())
				itemPos = itemPos.Rot(-r.Ang())
				if rayPos.X() < itemPos.X() {
					continue
				}
				if itemPos.Y() > 0.5 || itemPos.Y() < -0.5 {
					continue
				}
				dist := math.Sin(math.Pi/2-r.relAng) * itemPos.X()
				r.items = append(r.items, newRayItem(i.TypeID(), dist, itemPos.Y(), i.GetState(player)))
			}
		}
	}
}

// Rot rotates the ray by rad radians.
func (r *Ray) Rot(rad float64) {
	r.vector2dAng = r.vector2dAng.Rot(rad)

	ang := r.Ang()
	if ang > math.Pi*1.5 || ang < math.Pi*0.5 {
		r.dirX = 1
	} else if ang > math.Pi*0.5 && ang < math.Pi*1.5 {
		r.dirX = -1
	} else {
		r.dirX = 0
	}

	if ang > 0 && ang < math.Pi {
		r.dirY = 1
	} else if ang > math.Pi && ang < math.Pi*2 {
		r.dirY = -1
	} else {
		r.dirY = 0
	}

	cosAng := math.Cos(ang)
	if cosAng != 0 {
		r.deltaDistX = math.Abs(1 / cosAng)
	} else {
		r.deltaDistX = math.Inf(1)
	}
	sinAng := math.Sin(ang)
	if sinAng != 0 {
		r.deltaDistY = math.Abs(1 / sinAng)
	} else {
		r.deltaDistY = math.Inf(1)
	}
}

// RayItem stores information about an item seen by the ray.
type RayItem struct {
	typeID int
	dist   float64
	offset float64
	state  int
}

func newRayItem(typeID int, dist, offset float64, state int) *RayItem {
	return &RayItem{typeID: typeID, dist: dist, offset: offset, state: state}
}

func (ri *RayItem) TypeID() int    { return ri.typeID }
func (ri *RayItem) Dist() float64  { return ri.dist }
func (ri *RayItem) Offset() float64 { return ri.offset }
func (ri *RayItem) State() int     { return ri.state }

// RayDoor stores information about a door seen by the ray.
type RayDoor struct {
	typeID     int
	dist       float64
	offset     float64
	isVertical bool
}

func newRayDoor(dist, offset float64, isVertical bool) *RayDoor {
	return &RayDoor{typeID: 49, dist: dist, offset: offset, isVertical: isVertical}
}

func (rd *RayDoor) TypeID() int     { return rd.typeID }
func (rd *RayDoor) Dist() float64   { return rd.dist }
func (rd *RayDoor) Offset() float64 { return rd.offset }
func (rd *RayDoor) IsVertical() bool { return rd.isVertical }
func (rd *RayDoor) State() int {
	if rd.isVertical {
		return 1
	}
	return 0
}
