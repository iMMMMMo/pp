package edu.put.weatherapp

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import edu.put.weatherapp.model.ForecastItem
import java.text.SimpleDateFormat
import java.util.Locale

class HourlyForecastAdapter(private var forecastItems: List<ForecastItem>) :
    RecyclerView.Adapter<HourlyForecastAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_hourly_forecast, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = forecastItems[position]
        val sdf = SimpleDateFormat("HH:mm", Locale.getDefault())
        holder.timeTextView.text = sdf.format(item.dt * 1000)
        holder.hourlyTemperatureTextView.text = String.format("%.1f°C", item.main.temp)
        setWeatherIcon(holder.hourlyWeatherIcon, item.weather[0].icon)
        holder.hourlyWindSpeedTextView.text = "${item.wind.speed} km/h"
    }

    override fun getItemCount(): Int {
        return forecastItems.size
    }

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val timeTextView: TextView = view.findViewById(R.id.timeTextView)
        val hourlyTemperatureTextView: TextView = view.findViewById(R.id.hourlyTemperatureTextView)
        val hourlyWeatherIcon: ImageView = view.findViewById(R.id.hourlyWeatherIcon)
        val hourlyWindSpeedTextView: TextView = view.findViewById(R.id.hourlyWindSpeedTextView)
    }

    private fun setWeatherIcon(weatherIcon: ImageView, iconCode: String) {
        val iconRes = when (iconCode) {
            "01d", "01n" -> R.drawable.ic_sunny_12
            "02d", "02n", "03d", "03n", "04d", "04n" -> R.drawable.ic_cloud_12
            "09d", "09n", "10d", "10n" -> R.drawable.ic_rainy_12
            "13d", "13n" -> R.drawable.ic_snowing_12
            else -> R.drawable.ic_cloud_12
        }
        weatherIcon.setImageResource(iconRes)
    }

    fun updateForecastItems(newItems: List<ForecastItem>) {
        forecastItems = newItems
        notifyDataSetChanged()
    }
}
