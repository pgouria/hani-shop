from django.test import SimpleTestCase

from .domain import events


class EventSystemTests(SimpleTestCase):
    def setUp(self):
        events.SUBSCRIBTION.clear()

    def test_subscribe_registers_callback(self):
        callback = lambda: None

        events.subscribe("event-key", callback)

        self.assertIn("event-key", events.SUBSCRIBTION)
        self.assertEqual(events.SUBSCRIBTION["event-key"], [callback])

    def test_publish_calls_registered_callbacks(self):
        called = {"count": 0}

        def callback():
            called["count"] += 1

        events.subscribe("event-key", callback)

        events.publish("event-key")

        self.assertEqual(called["count"], 1)
