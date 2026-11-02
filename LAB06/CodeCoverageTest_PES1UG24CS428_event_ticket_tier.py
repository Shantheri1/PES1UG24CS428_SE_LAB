
import pytest

from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


# 1. General ticket with service tax
def test_general_ticket():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 2, "promo": ""}]
    }]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"


# 2. VIP ticket
def test_vip_ticket():
    manifests = [{
        "is_confirmed": True,
        "tier": "vip",
        "orders": [{"qty": 2}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["total_revenue"] == 300.0


# 3. Premium ticket
def test_premium_ticket():
    manifests = [{
        "is_confirmed": True,
        "tier": "premium",
        "orders": [{"qty": 2}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["total_revenue"] == 180.0


# 4. Unconfirmed booking
def test_unconfirmed_booking():
    manifests = [{
        "is_confirmed": False,
        "tier": "general",
        "orders": [{"qty": 2}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


# 5. Invalid ticket tier
def test_invalid_tier():
    manifests = [{
        "is_confirmed": True,
        "tier": "invalid",
        "orders": [{"qty": 2}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


# 6. Zero quantity
def test_zero_quantity():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 0}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


# 7. Negative quantity
def test_negative_quantity():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": -2}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


# 8. Earlybird promotion
def test_earlybird_promotion():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 2, "promo": "EARLYBIRD"}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["total_revenue"] == 72.0


# 9. Fraud risk promotion
def test_fraud_risk_general():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 2, "promo": "FRAUD_RISK"}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


# 10. VIP fraud risk
def test_fraud_risk_vip():
    manifests = [{
        "is_confirmed": True,
        "tier": "vip",
        "orders": [
            {"qty": 2, "promo": "FRAUD_RISK"},
            {"qty": 3}
        ]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


# 11. Bulk order discount
def test_bulk_order_discount():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 5}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["total_revenue"] == 205.0


# 12. Exclusive lounge charge
def test_lounge_charge():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "exclusive_lounge": True,
        "orders": [{"qty": 2}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["total_revenue"] == 165.0


# 13. More than four rejected orders
def test_more_than_four_rejections():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "invalid",
            "orders": []
        }
        for _ in range(5)
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "AUDIT_REJECTED"


# 14. Empty manifest list
def test_empty_manifest():
    result = process_ticket_manifest([], 0)
    assert result["status"] == "ZERO_SALES"


# 15. Invalid manifest input
def test_invalid_manifest_input():
    with pytest.raises(ValueError):
        process_ticket_manifest("invalid", 0)


# 16. Negative service tax
def test_negative_tax():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


# 17. No turnstile data
def test_no_turnstile_data():
    assert monitor_gate_flow([]) == "NO_DATA"


# 18. Normal gate flow
def test_normal_gate_flow():
    streams = [[30, 60, 40, 70, 30]]
    assert monitor_gate_flow(streams) == "FLOW_NORMAL"


# 19. Consecutive high gate flow
def test_consecutive_high_gate_flow():
    streams = [[60, 65, 40]]
    assert monitor_gate_flow(streams) == "OVERFLOW"


# 20. Default ticket tier
def test_default_ticket_tier():
    manifests = [{
        "is_confirmed": True,
        "orders": [{"qty": 1}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["total_revenue"] == 45.0
    assert result["status"] == "COMPLETED"


# 21. Empty orders
def test_empty_orders():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": []
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


# 22. Missing confirmation field
def test_missing_confirmation():
    manifests = [{
        "tier": "general",
        "orders": [{"qty": 2}]
    }]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"
