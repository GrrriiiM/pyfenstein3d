// capture renders scripted game frames to PNG images and an animated GIF,
// saving all output under the docs/captures/ directory relative to the repo root.
package main

import (
	"fmt"
	stdraw "image/draw"
	"image/gif"
	"image/png"
	"os"
	"path/filepath"
	"runtime"

	"image"
	"image/color/palette"

	xdraw "golang.org/x/image/draw"

	"pyfenstein3d/engine"
	"pyfenstein3d/game"
)

func main() {
	_, selfFile, _, ok := runtime.Caller(0)
	if !ok {
		fmt.Fprintln(os.Stderr, "error: could not determine source path")
		os.Exit(1)
	}
	// selfFile is go/cmd/capture/main.go; repo root is three levels up.
	repoDir := filepath.Join(filepath.Dir(selfFile), "..", "..", "..")
	assetsDir := filepath.Join(repoDir, "pyfenstein3d")
	outDir := filepath.Join(repoDir, "docs", "captures")

	if err := os.MkdirAll(outDir, 0o755); err != nil {
		fmt.Fprintf(os.Stderr, "error creating output dir: %v\n", err)
		os.Exit(1)
	}

	img, err := game.NewImage(assetsDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error loading sprites: %v\n", err)
		os.Exit(1)
	}

	hudPath := filepath.Join(assetsDir, "imgs", "hud.png")
	screen, err := game.NewScreen(img, hudPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error creating screen: %v\n", err)
		os.Exit(1)
	}

	server := engine.NewServer()
	mapFile := filepath.Join(assetsDir, "maps_pattern", "map_1_level_1.txt")
	if err := server.LoadMapFile(mapFile); err != nil {
		fmt.Fprintf(os.Stderr, "error loading map: %v\n", err)
		os.Exit(1)
	}

	const loopTime = 0.1 // 1 / FramesPerSecond (10 fps)
	const scale = 6      // upscale factor for readability

	pid := "123"
	pal := palette.Plan9 // 256-colour palette

	// gifFrames accumulates every rendered frame for the animated GIF.
	var gifFrames []*image.Paletted
	var gifDelays []int

	snap := func(label string) {
		player := server.GetPlayerState(pid)
		frame := screen.RenderFrame(player)

		// Scale up for visibility.
		scaledW := frame.Bounds().Dx() * scale
		scaledH := frame.Bounds().Dy() * scale
		scaled := image.NewNRGBA(image.Rect(0, 0, scaledW, scaledH))
		xdraw.ApproxBiLinear.Scale(scaled, scaled.Bounds(), frame, frame.Bounds(), xdraw.Src, nil)

		// Save PNG.
		pngPath := filepath.Join(outDir, label+".png")
		f, err := os.Create(pngPath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "error creating %s: %v\n", pngPath, err)
			return
		}
		if err := png.Encode(f, scaled); err != nil {
			f.Close()
			fmt.Fprintf(os.Stderr, "error encoding PNG %s: %v\n", pngPath, err)
			return
		}
		f.Close()
		fmt.Printf("saved %s\n", pngPath)

		// Accumulate GIF frame (use smaller size for GIF).
		gifW := frame.Bounds().Dx() * 3
		gifH := frame.Bounds().Dy() * 3
		gifScaled := image.NewNRGBA(image.Rect(0, 0, gifW, gifH))
		xdraw.ApproxBiLinear.Scale(gifScaled, gifScaled.Bounds(), frame, frame.Bounds(), xdraw.Src, nil)
		pImg := image.NewPaletted(gifScaled.Bounds(), pal)
		stdraw.Draw(pImg, pImg.Bounds(), gifScaled, image.Point{}, stdraw.Src)
		gifFrames = append(gifFrames, pImg)
		gifDelays = append(gifDelays, 10) // 10 × 10ms = 100ms per frame
	}

	type action struct {
		label    string
		frames   int
		snapAll  bool
		setup    func()
		teardown func()
	}

	actions := []action{
		{
			label:    "01_inicio",
			frames:   1,
			setup:    func() {},
			teardown: func() {},
		},
		{
			label:    "02_andando_frente",
			frames:   15,
			snapAll:  true,
			setup:    func() { server.PlayerStartMovingFront(pid) },
			teardown: func() { server.PlayerStopMovingFront(pid) },
		},
		{
			label:    "03_virando_direita",
			frames:   10,
			snapAll:  true,
			setup:    func() { server.PlayerStartTurningRight(pid) },
			teardown: func() { server.PlayerStopTurningRight(pid) },
		},
		{
			label:    "04_andando_frente2",
			frames:   12,
			snapAll:  true,
			setup:    func() { server.PlayerStartMovingFront(pid) },
			teardown: func() { server.PlayerStopMovingFront(pid) },
		},
		{
			label:    "05_virando_esquerda",
			frames:   8,
			snapAll:  true,
			setup:    func() { server.PlayerStartTurningLeft(pid) },
			teardown: func() { server.PlayerStopTurningLeft(pid) },
		},
		{
			label:    "06_atirando",
			frames:   10,
			snapAll:  true,
			setup:    func() { server.PlayerStartShooting(pid) },
			teardown: func() { server.PlayerStopShooting(pid) },
		},
	}

	// Tick the engine once so the FOV is initialised.
	server.Update(loopTime)
	snap("00_titulo")

	for _, a := range actions {
		a.setup()
		for i := 0; i < a.frames; i++ {
			server.Update(loopTime)
			if a.snapAll {
				snap(fmt.Sprintf("%s_f%02d", a.label, i))
			} else if i == 0 || i == a.frames-1 {
				snap(a.label)
			}
		}
		a.teardown()
	}

	// Write animated GIF.
	gifPath := filepath.Join(outDir, "walkthrough.gif")
	gf, err := os.Create(gifPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error creating GIF: %v\n", err)
		os.Exit(1)
	}
	if err := gif.EncodeAll(gf, &gif.GIF{
		Image:     gifFrames,
		Delay:     gifDelays,
		LoopCount: 0,
	}); err != nil {
		gf.Close()
		fmt.Fprintf(os.Stderr, "error encoding GIF: %v\n", err)
		os.Exit(1)
	}
	gf.Close()
	fmt.Printf("saved %s (%d frames)\n", gifPath, len(gifFrames))
}
