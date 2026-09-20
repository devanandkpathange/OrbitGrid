"""
Unit tests for GridPoint mathematical optimization engine and distance models.
"""

import unittest
from backend.services.maps import (
    haversine_distance_km, 
    indian_road_distance_km, 
    INDIAN_ROAD_CIRCUITY_FACTOR
)
from backend.models.india_hubs import find_nearest_hub
from backend.optimization.cost_model import (
    calculate_delivery_cost_inr, 
    calculate_green_logistics_metrics
)
from backend.optimization.optimizer import (
    weiszfeld_single_facility,
    solve_weighted_k_medoids,
    optimize_warehouse_network,
    compute_baseline_benchmark,
    compute_elbow_curve
)


class TestOptimizationEngine(unittest.TestCase):

    def setUp(self):
        # Sample Karnataka demand points
        self.karnataka_demand = [
            {"id": "blr_south", "name": "Bengaluru South", "lat": 12.8452, "lng": 77.6602, "demand": 14200},
            {"id": "blr_north", "name": "Bengaluru North", "lat": 13.0358, "lng": 77.5970, "demand": 16800},
            {"id": "mysuru", "name": "Mysuru", "lat": 12.2958, "lng": 76.6394, "demand": 8400},
            {"id": "hubballi", "name": "Hubballi", "lat": 15.3647, "lng": 75.1240, "demand": 9200},
            {"id": "belagavi", "name": "Belagavi", "lat": 15.8497, "lng": 74.4977, "demand": 6800}
        ]

    def test_indian_road_circuity(self):
        # Bengaluru to Mysuru straight-line is ~125 km, road distance ~140-160 km
        h_dist = haversine_distance_km(12.9716, 77.5946, 12.2958, 76.6394)
        r_dist = indian_road_distance_km(12.9716, 77.5946, 12.2958, 76.6394)
        self.assertGreater(r_dist, h_dist)
        self.assertAlmostEqual(r_dist, h_dist * INDIAN_ROAD_CIRCUITY_FACTOR, places=1)

    def test_weiszfeld_gravity_center(self):
        pts = [(d["lat"], d["lng"], d["demand"]) for d in self.karnataka_demand]
        c_lat, c_lng = weiszfeld_single_facility(pts)
        # Centroid should lie between 12.0 and 16.0 lat, 74.0 and 78.0 lng
        self.assertTrue(12.0 <= c_lat <= 16.0)
        self.assertTrue(74.0 <= c_lng <= 78.0)

    def test_hub_snapping(self):
        # Near Bengaluru: should snap to a recognized Bengaluru cluster
        hub = find_nearest_hub(12.9716, 77.5946, state="Karnataka")
        self.assertIsNotNone(hub)
        self.assertIn("Bengaluru", hub["city"])
        self.assertIn("typical_rent_sqft_inr", hub)

    def test_k_medoids_2_warehouses(self):
        whs = solve_weighted_k_medoids(self.karnataka_demand, k=2)
        self.assertEqual(len(whs), 2)
        self.assertEqual(whs[0]["id"], "WH1")
        self.assertEqual(whs[1]["id"], "WH2")

    def test_full_optimization_pipeline(self):
        result = optimize_warehouse_network(
            demand_points=self.karnataka_demand,
            warehouse_count=2,
            region="Karnataka"
        )
        self.assertIn("warehouses", result)
        self.assertIn("assignments", result)
        self.assertIn("metrics", result)
        self.assertIn("geojson_catchment", result)

        self.assertEqual(len(result["warehouses"]), 2)
        self.assertEqual(len(result["assignments"]), len(self.karnataka_demand))
        self.assertGreater(result["metrics"]["total_cost"], 0)
        self.assertEqual(result["metrics"]["currency"], "INR")
        self.assertGreater(result["metrics"]["co2_emissions_kg"], 0)

    def test_capacity_constraints(self):
        # Set tight capacity: 20,000 units max per warehouse
        result = optimize_warehouse_network(
            demand_points=self.karnataka_demand,
            warehouse_count=3,
            capacity_limit=25000.0
        )
        for wh in result["warehouses"]:
            self.assertLessEqual(wh["assigned_demand"], 25000.0)

    def test_baseline_benchmark(self):
        opt = optimize_warehouse_network(
            demand_points=self.karnataka_demand,
            warehouse_count=2
        )
        bench = compute_baseline_benchmark(self.karnataka_demand, opt)
        self.assertIn("before", bench)
        self.assertIn("after", bench)
        self.assertIn("comparisons", bench)
        self.assertIn("summary", bench)

    def test_elbow_curve(self):
        elbow = compute_elbow_curve(self.karnataka_demand, max_k=4)
        self.assertEqual(elbow["region"], "Karnataka")
        self.assertGreaterEqual(len(elbow["points"]), 2)
        self.assertTrue(any(p["is_recommended"] for p in elbow["points"]))


if __name__ == "__main__":
    unittest.main()
