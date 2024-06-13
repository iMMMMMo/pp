package edu.put.weatherapp

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import android.os.Bundle
import android.os.PowerManager
import android.view.inputmethod.EditorInfo
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import androidx.appcompat.widget.Toolbar
import android.widget.TextView
import android.widget.EditText
import android.view.Menu
import android.view.MenuItem
import android.widget.ImageView
import android.widget.Toast
import com.google.android.gms.location.*
import com.google.firebase.firestore.FirebaseFirestore
import edu.put.weatherapp.network.RetrofitClient
import edu.put.weatherapp.network.WeatherApiService
import edu.put.weatherapp.model.ForecastItem
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var cityTextView: TextView
    private lateinit var lastUpdatedTextView: TextView
    private lateinit var cityEditText: EditText
    private lateinit var temperatureTextView: TextView
    private lateinit var weatherDescriptionTextView: TextView
    private lateinit var hourlyForecastRecyclerView: RecyclerView
    private lateinit var swipeRefreshLayout: SwipeRefreshLayout
    private lateinit var toolbar: Toolbar
    private lateinit var hourlyForecastAdapter: HourlyForecastAdapter
    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private lateinit var firestore: FirebaseFirestore
    private lateinit var weatherIcon: ImageView

    private val weatherApiService: WeatherApiService by lazy {
        RetrofitClient.instance.create(WeatherApiService::class.java)
    }

    companion object {
        private const val LOCATION_PERMISSION_REQUEST_CODE = 1
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        toolbar = findViewById(R.id.toolbar)
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayShowTitleEnabled(false)

        cityTextView = findViewById(R.id.cityTextView)
        lastUpdatedTextView = findViewById(R.id.lastUpdatedTextView)
        cityEditText = findViewById(R.id.cityEditText)
        temperatureTextView = findViewById(R.id.temperatureTextView)
        weatherDescriptionTextView = findViewById(R.id.weatherDescriptionTextView)
        hourlyForecastRecyclerView = findViewById(R.id.hourlyForecastRecyclerView)
        swipeRefreshLayout = findViewById(R.id.swipeRefreshLayout)

        hourlyForecastRecyclerView.layoutManager = LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false)
        hourlyForecastAdapter = HourlyForecastAdapter(emptyList())
        hourlyForecastRecyclerView.adapter = hourlyForecastAdapter

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)

        firestore = FirebaseFirestore.getInstance()

        weatherIcon = findViewById(R.id.weatherIcon)

        cityEditText.setOnEditorActionListener { v, actionId, event ->
            if (actionId == EditorInfo.IME_ACTION_DONE) {
                if (isInternetAvailable()) {
                    updateWeatherData(cityEditText.text.toString())
                } else {
                    showToast("No internet connection.")
                }
                true
            } else {
                updateWeatherData(cityEditText.text.toString())
                true
            }
        }

        val searchIcon: ImageView = findViewById(R.id.ic_search_12)
        searchIcon.setOnClickListener {
            if (isInternetAvailable()) {
                updateWeatherData(cityEditText.text.toString())
            } else {
                showToast("No internet connection.")
            }
        }

        swipeRefreshLayout.setOnRefreshListener {
            if (isInternetAvailable()) {
                updateWeatherData(cityEditText.text.toString())
            } else {
                showToast("No internet connection.")
                swipeRefreshLayout.isRefreshing = false
            }
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.ACCESS_COARSE_LOCATION), LOCATION_PERMISSION_REQUEST_CODE)
        } else {
            if (isLocationEnabled()) {
                getLastLocation()
            } else {
                showToast("Location is disabled.")
            }
        }

        if (isInternetAvailable() and !isLocationEnabled()) {
            updateWeatherData("Warsaw")
        }
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.toolbar_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_history -> {
                val intent = Intent(this, HistoryActivity::class.java)
                startActivity(intent)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun updateWeatherData(city: String) {
        if (!isInternetAvailable()) {
            showToast("No internet connection.")
            return
        }
        val apiKey = "22af04d3b2141fdf9cc453cb93b2378b"
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val weatherResponse = weatherApiService.getCurrentWeather(city, apiKey)
                val forecastResponse = weatherApiService.getForecast(city, apiKey)

                withContext(Dispatchers.Main) {
                    cityTextView.text = weatherResponse.name
                    temperatureTextView.text = String.format("%.1f°C", weatherResponse.main.temp)
                    weatherDescriptionTextView.text = weatherResponse.weather[0].description.capitalize()
                    val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())
                    val currentDateAndTime = sdf.format(Date())
                    lastUpdatedTextView.text = "Last updated: $currentDateAndTime"

                    val forecastItems = forecastResponse.list.take(8)
                    hourlyForecastAdapter.updateForecastItems(forecastItems)

                    saveCityToHistory(weatherResponse.name)

                    setWeatherIcon(weatherResponse.weather[0].icon)

                    swipeRefreshLayout.isRefreshing = false
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) {
                    swipeRefreshLayout.isRefreshing = false
                    showToast("City does not exist.")
                }
            }
        }
    }

    private fun updateWeatherDataWithCoordinates(latitude: Double, longitude: Double) {
        val apiKey = "22af04d3b2141fdf9cc453cb93b2378b"
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val weatherResponse = weatherApiService.getCurrentWeatherByCoordinates(latitude, longitude, apiKey)
                val forecastResponse = weatherApiService.getForecastByCoordinates(latitude, longitude, apiKey)

                withContext(Dispatchers.Main) {
                    cityTextView.text = weatherResponse.name
                    temperatureTextView.text = String.format("%.1f°C", weatherResponse.main.temp)
                    weatherDescriptionTextView.text = weatherResponse.weather[0].description.capitalize()
                    val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())
                    val currentDateAndTime = sdf.format(Date())
                    lastUpdatedTextView.text = "Last updated: $currentDateAndTime"

                    val forecastItems = forecastResponse.list.take(8)
                    hourlyForecastAdapter.updateForecastItems(forecastItems)

                    saveCityToHistory(weatherResponse.name)

                    setWeatherIcon(weatherResponse.weather[0].icon)

                    swipeRefreshLayout.isRefreshing = false
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) {
                    swipeRefreshLayout.isRefreshing = false
                    showToast("Error: ${e.message}")
                }
            }
        }
    }

    private fun saveCityToHistory(city: String) {
        val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())
        val currentDateAndTime = sdf.format(Date())
        val history = hashMapOf(
            "city" to city,
            "dateTime" to currentDateAndTime
        )
        firestore.collection("history")
            .add(history)
            .addOnSuccessListener { documentReference ->
                println("Dodano historię z ID: ${documentReference.id}")
            }
            .addOnFailureListener { e ->
                println("Błąd dodawania historii: $e")
            }
    }

    private fun getLastLocation() {
        if (!isInternetAvailable()) {
            showToast("No internet connection.")
            return
        }
        if (!isLocationEnabled()) {
            showToast("Location is disabled.")
            return
        }
        fusedLocationClient.lastLocation.addOnSuccessListener { location: Location? ->
            if (location != null) {
                val latitude = location.latitude
                val longitude = location.longitude
                updateWeatherDataWithCoordinates(latitude, longitude)
            }
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show()
    }

    private fun setWeatherIcon(iconCode: String) {
        val iconRes = when (iconCode) {
            "01d", "01n" -> R.drawable.ic_sunny_12
            "02d", "02n", "03d", "03n", "04d", "04n" -> R.drawable.ic_cloud_12
            "09d", "09n", "10d", "10n" -> R.drawable.ic_rainy_12
            "13d", "13n" -> R.drawable.ic_snowing_12
            else -> R.drawable.ic_cloud_12
        }
        weatherIcon.setImageResource(iconRes)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        when (requestCode) {
            LOCATION_PERMISSION_REQUEST_CODE -> {
                if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                    getLastLocation()
                } else {
                    showToast("Permission denied. Cannot retrieve location data.")
                }
                return
            }
        }
    }

    private fun isInternetAvailable(): Boolean {
        val connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val network = connectivityManager.activeNetwork ?: return false
            val activeNetwork = connectivityManager.getNetworkCapabilities(network) ?: return false
            return when {
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> true
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> true
                else -> false
            }
        } else {
            @Suppress("DEPRECATION")
            val networkInfo = connectivityManager.activeNetworkInfo
            @Suppress("DEPRECATION")
            return networkInfo != null && networkInfo.isConnected
        }
    }

    private fun isLocationEnabled(): Boolean {
        val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER)
    }

}
