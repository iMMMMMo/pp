package edu.put.weatherapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.firebase.firestore.FirebaseFirestore

class HistoryActivity : AppCompatActivity() {

    private lateinit var historyRecyclerView: RecyclerView
    private lateinit var historyAdapter: HistoryAdapter
    private lateinit var firestore: FirebaseFirestore

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_history)

        val toolbar: androidx.appcompat.widget.Toolbar = findViewById(R.id.toolbar)
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        historyRecyclerView = findViewById(R.id.historyRecyclerView)
        historyRecyclerView.layoutManager = LinearLayoutManager(this)

        firestore = FirebaseFirestore.getInstance()

        historyAdapter = HistoryAdapter(emptyList())
        historyRecyclerView.adapter = historyAdapter

        loadHistory()
    }

    private fun loadHistory() {
        firestore.collection("history")
            .orderBy("dateTime", com.google.firebase.firestore.Query.Direction.DESCENDING)
            .get()
            .addOnSuccessListener { result ->
                historyAdapter.updateHistory(result.documents)
            }
            .addOnFailureListener { exception ->
                // Loguj błąd
                println("Błąd pobierania historii: $exception")
            }
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
