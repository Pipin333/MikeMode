# 🧪 Patrones de Testing Modernos por Ecosistema

Guía de patrones idiomáticos para redactar pruebas reproducibles, rápidas y deterministas.

---

## 1. Python (`pytest`)

### A. Test Parametrizado para Casos Borde y Regresiones
```python
import pytest
from app.calculator import parse_currency

@pytest.mark.parametrize("raw_input, expected_amount, expected_currency", [
    ("$100.50", 100.50, "USD"),
    ("€ 45,00", 45.00, "EUR"),
    ("¥1000", 1000.0, "JPY"),
    ("0.00", 0.0, "USD"),
])
def test_parse_currency_valid_formats(raw_input: str, expected_amount: float, expected_currency: str):
    amount, currency = parse_currency(raw_input)
    assert amount == pytest.approx(expected_amount)
    assert currency == expected_currency

def test_parse_currency_invalid_format_raises_value_error():
    with pytest.raises(ValueError, match="Formato no reconocido"):
        parse_currency("invalido_123")
```

### B. Uso de Fixtures y Aislamiento de Entorno
```python
import pytest
from app.db import DatabaseSession

@pytest.fixture
def clean_db(tmp_path):
    """Crea una base de datos aislada en memoria o carpeta temporal para el test."""
    db_file = tmp_path / "test.db"
    session = DatabaseSession(f"sqlite:///{db_file}")
    session.create_tables()
    yield session
    session.close()

def test_user_creation_persists_correctly(clean_db):
    user = clean_db.create_user(email="test@example.com")
    assert user.id is not None
    assert clean_db.get_user(user.id).email == "test@example.com"
```

---

## 2. TypeScript / JavaScript (`Vitest` o `Jest`)

### A. Pruebas Asíncronas y Manejo de Errores
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchUserData } from './userService';

describe('fetchUserData', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('debe transformar la respuesta correctamente cuando la API responde 200', async () => {
    const mockFetch = vi.spyOn(global, 'fetch').mockResolvedValueOnce(
      new Response(JSON.stringify({ id: 1, name: 'Alice' }), { status: 200 })
    );

    const user = await fetchUserData(1);
    expect(user).toEqual({ id: 1, name: 'Alice' });
    expect(mockFetch).toHaveBeenCalledWith('/api/users/1', expect.any(Object));
  });

  it('debe arrojar UserNotFoundError ante respuestas con código 404', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce(
      new Response(null, { status: 404 })
    );

    await expect(fetchUserData(999)).rejects.toThrow('Usuario no encontrado');
  });
});
```

---

## 3. Go (`testing` con Table-Driven Tests)

```go
package service_test

import (
	"testing"
	"myapp/service"
)

func TestValidateEmail(t *testing.T) {
	tests := []struct {
		name    string
		email   string
		wantErr bool
	}{
		{name: "email válido estándar", email: "user@example.com", wantErr: false},
		{name: "email con subdominio", email: "user@mail.co.uk", wantErr: false},
		{name: "falta arroba", email: "userexample.com", wantErr: true},
		{name: "string vacío", email: "", wantErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := service.ValidateEmail(tt.email)
			if (err != nil) != tt.wantErr {
				t.Errorf("ValidateEmail(%q) error = %v, wantErr = %v", tt.email, err, tt.wantErr)
			}
		})
	}
}
```

---

## 4. Rust (`cargo test`)

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_token_decoding() {
        let raw = "header.payload.signature";
        let token = parse_token(raw).expect("El token válido debería procesarse");
        assert_eq!(token.user_id, 42);
    }

    #[test]
    fn test_expired_token_returns_error() {
        let expired = "header.expired_payload.signature";
        let result = parse_token(expired);
        assert!(matches!(result, Err(TokenError::Expired)));
    }
}
```
