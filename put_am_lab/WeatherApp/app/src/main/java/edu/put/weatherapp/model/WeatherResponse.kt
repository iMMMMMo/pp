package edu.put.weatherapp.model

import com.google.gson.annotations.SerializedName

data class WeatherResponse(
    val coord: Coord,
    val weather: List<Weather>,
    val main: Main,
    val wind: Wind,
    val clouds: Clouds,
    val dt: Long,
    val sys: Sys,
    val name: String,
    @SerializedName("dt_txt") val dateTimeText: String?
)

data class Coord(val lon: Double, val lat: Double)
data class Weather(val id: Int, val main: String, val description: String, val icon: String)
data class Main(val temp: Float, val feels_like: Float, val temp_min: Float, val temp_max: Float, val pressure: Int, val humidity: Int)
data class Wind(val speed: Float, val deg: Int)
data class Clouds(val all: Int)
data class Sys(val type: Int, val id: Int, val country: String, val sunrise: Long, val sunset: Long)
