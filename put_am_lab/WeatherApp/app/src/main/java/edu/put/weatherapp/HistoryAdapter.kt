package edu.put.weatherapp

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.google.firebase.firestore.DocumentSnapshot

class HistoryAdapter(private var historyList: List<DocumentSnapshot>) :
    RecyclerView.Adapter<HistoryAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_history, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = historyList[position]
        holder.cityTextView.text = item.getString("city")
        holder.dateTimeTextView.text = item.getString("dateTime")
    }

    override fun getItemCount(): Int {
        return historyList.size
    }

    fun updateHistory(newHistoryList: List<DocumentSnapshot>) {
        historyList = newHistoryList
        notifyDataSetChanged()
    }

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val cityTextView: TextView = view.findViewById(R.id.cityTextView)
        val dateTimeTextView: TextView = view.findViewById(R.id.dateTimeTextView)
    }
}
