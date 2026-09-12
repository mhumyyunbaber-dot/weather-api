from app.database import usage_collection


class AnalyticsService:

    async def get_usage_summary(self) -> dict:

        pipeline = [
            {
                "$group": {
                    "_id": None,

                    "total_requests": {
                        "$sum": 1
                    },

                    "successful_requests": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {
                                            "$gte": [
                                                "$status_code",
                                                200
                                            ]
                                        },
                                        {
                                            "$lt": [
                                                "$status_code",
                                                400
                                            ]
                                        }
                                    ]
                                },
                                1,
                                0
                            ]
                        }
                    },

                    "failed_requests": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$gte": [
                                        "$status_code",
                                        400
                                    ]
                                },
                                1,
                                0
                            ]
                        }
                    },

                    "average_response_time": {
                        "$avg": "$response_time_ms"
                    }
                }
            }
        ]

        cursor = await usage_collection.aggregate(
            pipeline
        )

        result = await cursor.to_list(
            length=1
        )

        if not result:
            return {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0
            }

        data = result[0]

        return {
            "total_requests": data["total_requests"],
            "successful_requests": data["successful_requests"],
            "failed_requests": data["failed_requests"],
            "average_response_time": round(
                data["average_response_time"],
                2
            )
        }


    async def get_endpoint_usage(self) -> list:

        pipeline = [
            {
                "$group": {
                    "_id": "$endpoint",

                    "total_requests": {
                        "$sum": 1
                    },

                    "successful_requests": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {
                                            "$gte": [
                                                "$status_code",
                                                200
                                            ]
                                        },
                                        {
                                            "$lt": [
                                                "$status_code",
                                                400
                                            ]
                                        }
                                    ]
                                },
                                1,
                                0
                            ]
                        }
                    },

                    "failed_requests": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$gte": [
                                        "$status_code",
                                        400
                                    ]
                                },
                                1,
                                0
                            ]
                        }
                    },

                    "average_response_time": {
                        "$avg": "$response_time_ms"
                    }
                }
            },
            {
                "$sort": {
                    "total_requests": -1
                }
            }
        ]

        cursor = await usage_collection.aggregate(
            pipeline
        )

        results = await cursor.to_list(
            length=None
        )

        return [
            {
                "endpoint": item["_id"],
                "total_requests": item["total_requests"],
                "successful_requests": item["successful_requests"],
                "failed_requests": item["failed_requests"],
                "average_response_time": round(
                    item["average_response_time"],
                    2
                )
            }
            for item in results
        ]