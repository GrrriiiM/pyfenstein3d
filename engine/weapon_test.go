package engine

import (
	"testing"
)

func TestWeaponShoot(t *testing.T) {
	weapon := NewWeapon(10, 0.5)
	player := NewPlayer(0, 0, 0, nil, "")

	if weapon.ShootInterval() != 0.5 {
		t.Errorf("shootInterval: expected 0.5, got %v", weapon.ShootInterval())
	}
	if weapon.IsShooting {
		t.Error("should not be shooting initially")
	}
	if weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should not be active initially")
	}
	assertApprox(t, 0, weapon.ShootAnimation().Factor(), "factor init")

	// update without shooting – nothing changes
	weapon.Update(0.1, player, nil)
	if weapon.IsShooting {
		t.Error("still should not be shooting")
	}
	if weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should still not be active")
	}
	assertApprox(t, 0, weapon.ShootAnimation().Factor(), "factor after no-shoot update")

	// start shooting
	weapon.IsShooting = true
	if !weapon.IsShooting {
		t.Error("IsShooting should be true")
	}

	weapon.Update(0.1, player, nil)
	if !weapon.IsShooting {
		t.Error("IsShooting should still be true")
	}
	if !weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should now be active")
	}
	assertApprox(t, 0.2, weapon.ShootAnimation().Factor(), "factor 0.2")

	weapon.Update(0.1, player, nil)
	if !weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should still be active")
	}
	assertApprox(t, 0.4, weapon.ShootAnimation().Factor(), "factor 0.4")

	weapon.Update(0.3, player, nil)
	if weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should have ended")
	}
	assertApprox(t, 1, weapon.ShootAnimation().Factor(), "factor 1")

	weapon.Update(0.3, player, nil)
	if !weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should restart after interval")
	}
	assertApprox(t, 0.6, weapon.ShootAnimation().Factor(), "factor 0.6")

	weapon.IsShooting = false
	weapon.Update(0.3, player, nil)
	if weapon.IsShooting {
		t.Error("IsShooting should be false")
	}
	if weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should have ended")
	}
	assertApprox(t, 1, weapon.ShootAnimation().Factor(), "factor end")

	weapon.Update(0.3, player, nil)
	if weapon.ShootAnimation().IsAnimating() {
		t.Error("animation should not restart when not shooting")
	}
	assertApprox(t, 0, weapon.ShootAnimation().Factor(), "factor reset")
}
