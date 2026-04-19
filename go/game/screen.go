package game

import (
	"fmt"
	"image"
	"image/color"
	"math"
	"os"
	"sort"
	"strings"

	"pyfenstein3d/engine"

	"golang.org/x/image/draw"
)

// Screen renders the game world to the terminal using ANSI true-colour escape codes.
type Screen struct {
	images   *Image
	hudImg   *image.NRGBA
	screenW  int
	screenH  int
	hudH     int
	pixelTpl string
}

// NewScreen creates a Screen backed by the given Image sprite manager.
// hudPath is the file-system path to the HUD PNG asset.
func NewScreen(images *Image, hudPath string) (*Screen, error) {
	rayCount := engine.RayCount

	s := &Screen{
		images:   images,
		screenW:  rayCount,
		screenH:  int(math.Floor(float64(rayCount) * 0.5)),
		hudH:     int(math.Floor(float64(rayCount) / 8)),
		pixelTpl: "\033[48;2;%d;%d;%dm  ",
	}

	f, err := os.Open(hudPath)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	decoded, _, err := image.Decode(f)
	if err != nil {
		return nil, err
	}
	bounds := decoded.Bounds()
	s.hudImg = image.NewNRGBA(bounds)
	draw.Copy(s.hudImg, image.Point{}, decoded, bounds, draw.Src, nil)

	return s, nil
}

// Draw renders a full frame to the terminal.
func (s *Screen) Draw(player *engine.Player) {
	pixelMatrix := s.createPixelMatrix(player)
	var sb strings.Builder
	sb.WriteString("\033[0;0H")
	for ph := 0; ph < s.screenH; ph++ {
		for pw := 0; pw < s.screenW; pw++ {
			px := pixelMatrix[ph][pw]
			fmt.Fprintf(&sb, s.pixelTpl, px[0], px[1], px[2])
		}
		if ph < s.screenH-1 {
			sb.WriteByte('\n')
		}
	}
	fmt.Fprint(os.Stdout, sb.String())
}

// rayObject holds a sorted list of doors and items for a single ray column.
type rayObject struct {
	isDoor bool
	dist   float64
	offset float64
	typeID int
	state  int
}

func (s *Screen) createPixelMatrix(player *engine.Player) [][][3]uint8 {
	img := CreateBackground(s.screenW, s.screenH)

	fov := player.Fov()
	rays := fov.Rays()
	for i := 0; i < s.screenW && i < len(rays); i++ {
		ray := rays[i]
		if ray.TypeID() == nil {
			continue
		}
		if ray.DistAdjusted() > 0 {
			height := int(math.Round(float64(s.screenH) * 2 / ray.DistAdjusted()))
			offset := int(math.Floor(ray.Offset() * 64))
			stateIdx := 0
			if ray.IsVertical() {
				stateIdx = 1
			}
			colImg := s.images.GetColumn(*ray.TypeID(), offset, height, stateIdx)
			pasteColumn(img, colImg, i, int(math.Floor(float64(s.screenH)/2-float64(height)/2)))

			var objs []rayObject
			for _, rd := range ray.Doors() {
				objs = append(objs, rayObject{isDoor: true, dist: rd.Dist(), offset: rd.Offset(), typeID: rd.TypeID(), state: rd.State()})
			}
			for _, ri := range ray.Items() {
				objs = append(objs, rayObject{isDoor: false, dist: ri.Dist(), offset: ri.Offset(), typeID: ri.TypeID(), state: ri.State()})
			}
			sort.Slice(objs, func(a, b int) bool { return objs[a].dist > objs[b].dist })

			for _, obj := range objs {
				if obj.dist <= 0.001 {
					continue
				}
				h := int(math.Round(float64(s.screenH) * 2 / obj.dist))
				var colI image.Image
				if obj.isDoor {
					off := int(math.Floor(obj.offset * 64))
					colI = s.images.GetColumn(49, off, h, obj.state)
				} else {
					off := int(math.Floor((obj.offset + 0.5) * 64))
					colI = s.images.GetColumn(obj.typeID, off, h, obj.state)
				}
				pasteColumnAlpha(img, colI, i, int(math.Floor(float64(s.screenH)/2-float64(h)/2)))
			}
		}
	}

	// Draw the weapon sprite.
	weapon := player.Weapon()
	wState := 0
	if weapon.ShootAnimation().IsAnimating() {
		f := weapon.ShootAnimation().Factor()
		switch {
		case f < 0.2:
			wState = 1
		case f < 0.3:
			wState = 2
		case f < 0.6:
			wState = 3
		default:
			wState = 4
		}
	}
	wImg := s.images.Get(weapon.TypeID(), 64, 64, wState)
	wBounds := wImg.Bounds()
	wX := int(math.Round(float64(s.screenW)/2 - float64(wBounds.Dx())/2))
	wY := s.screenH - wBounds.Dy()
	pasteImageAlpha(img, wImg, wX, wY)

	result := make([][][3]uint8, s.screenH)
	for ph := 0; ph < s.screenH; ph++ {
		result[ph] = make([][3]uint8, s.screenW)
		for pw := 0; pw < s.screenW; pw++ {
			r, g, b, _ := img.At(pw, ph).RGBA()
			result[ph][pw] = [3]uint8{uint8(r >> 8), uint8(g >> 8), uint8(b >> 8)}
		}
	}
	return result
}

// DrawHUD renders the heads-up display below the 3-D view.
func (s *Screen) DrawHUD() {
	const imgH = 40
	imgFactor := float64(imgH) / (float64(engine.RayCount) / 8)
	fmt.Fprintf(os.Stdout, "\033[%d;0H", s.screenH)

	var sb strings.Builder
	for ph := 0; ph < s.hudH; ph++ {
		for pw := 0; pw < s.screenW; pw++ {
			srcX := int(math.Floor(float64(pw) * imgFactor))
			srcY := int(math.Floor(float64(ph) * imgFactor))
			r, g, b, _ := s.hudImg.At(srcX, srcY).RGBA()
			fmt.Fprintf(&sb, s.pixelTpl, r>>8, g>>8, b>>8)
		}
		sb.WriteByte('\n')
	}
	fmt.Fprint(os.Stdout, sb.String())
}

// RenderFrame renders a full game frame (3-D view + HUD) into a new NRGBA image.
// The image is (screenW × (screenH + hudH)) pixels; each pixel corresponds to
// one terminal "pixel" (a 2-character block).
func (s *Screen) RenderFrame(player *engine.Player) *image.NRGBA {
	pm := s.createPixelMatrix(player)
	totalH := s.screenH + s.hudH
	out := image.NewNRGBA(image.Rect(0, 0, s.screenW, totalH))

	for ph := 0; ph < s.screenH; ph++ {
		for pw := 0; pw < s.screenW; pw++ {
			px := pm[ph][pw]
			out.SetNRGBA(pw, ph, color.NRGBA{R: px[0], G: px[1], B: px[2], A: 255})
		}
	}

	const imgH = 40
	imgFactor := float64(imgH) / (float64(engine.RayCount) / 8)
	for ph := 0; ph < s.hudH; ph++ {
		for pw := 0; pw < s.screenW; pw++ {
			srcX := int(math.Floor(float64(pw) * imgFactor))
			srcY := int(math.Floor(float64(ph) * imgFactor))
			r, g, b, a := s.hudImg.At(srcX, srcY).RGBA()
			out.SetNRGBA(pw, s.screenH+ph, color.NRGBA{
				R: uint8(r >> 8), G: uint8(g >> 8), B: uint8(b >> 8), A: uint8(a >> 8),
			})
		}
	}
	return out
}

// pasteColumn copies all pixels from a single-column image src into dst at (x, dstY).
func pasteColumn(dst *image.NRGBA, src image.Image, x, dstY int) {
	bounds := src.Bounds()
	h := bounds.Dy()
	for y := 0; y < h; y++ {
		dstPY := dstY + y
		if dstPY < 0 || dstPY >= dst.Bounds().Dy() {
			continue
		}
		r, g, b, a := src.At(bounds.Min.X, bounds.Min.Y+y).RGBA()
		dst.SetNRGBA(x, dstPY, color.NRGBA{
			R: uint8(r >> 8), G: uint8(g >> 8), B: uint8(b >> 8), A: uint8(a >> 8),
		})
	}
}

// pasteColumnAlpha copies pixels with alpha blending (items/doors with transparency).
func pasteColumnAlpha(dst *image.NRGBA, src image.Image, x, dstY int) {
	bounds := src.Bounds()
	h := bounds.Dy()
	for y := 0; y < h; y++ {
		dstPY := dstY + y
		if dstPY < 0 || dstPY >= dst.Bounds().Dy() {
			continue
		}
		sr, sg, sb, sa := src.At(bounds.Min.X, bounds.Min.Y+y).RGBA()
		if sa == 0 {
			continue
		}
		dst.SetNRGBA(x, dstPY, color.NRGBA{
			R: uint8(sr >> 8), G: uint8(sg >> 8), B: uint8(sb >> 8), A: uint8(sa >> 8),
		})
	}
}

// pasteImageAlpha blits src onto dst at (dstX, dstY) respecting alpha.
func pasteImageAlpha(dst *image.NRGBA, src image.Image, dstX, dstY int) {
	b := src.Bounds()
	for y := b.Min.Y; y < b.Max.Y; y++ {
		for x := b.Min.X; x < b.Max.X; x++ {
			sr, sg, sb, sa := src.At(x, y).RGBA()
			if sa == 0 {
				continue
			}
			dstPX := dstX + (x - b.Min.X)
			dstPY := dstY + (y - b.Min.Y)
			if dstPX < 0 || dstPX >= dst.Bounds().Dx() || dstPY < 0 || dstPY >= dst.Bounds().Dy() {
				continue
			}
			dst.SetNRGBA(dstPX, dstPY, color.NRGBA{
				R: uint8(sr >> 8), G: uint8(sg >> 8), B: uint8(sb >> 8), A: uint8(sa >> 8),
			})
		}
	}
}
