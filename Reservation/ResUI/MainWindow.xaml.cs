using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ResUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        public string token { get; set; }
        public string res_name { get; set; }

        public MainWindow()
        {
            InitializeComponent();
        }


        public MainWindow( string restaurant_name, string token)
        {
            InitializeComponent();
            ResName.Text = "Hi, " + restaurant_name;
           
            
            this.res_name = restaurant_name.ToLower();
            this.token = token;
            
        }


        private async void LoadContents(string res_name, string token)
        {
            //while (true)
            {
                HttpClient client = new HttpClient();
                string uri = $"http://localhost:5000/restrv1/{res_name}/{token}/available";
                HttpResponseMessage response = await client.GetAsync(uri);
                response.EnsureSuccessStatusCode();
                string responseString = await response.Content.ReadAsStringAsync();
                List<TimeSlot> timeSlots = JsonConvert.DeserializeObject<List<TimeSlot>>(responseString);
                lvSlots.ItemsSource = timeSlots;
            }            
        }

        public void TabControl_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (Reservation.IsSelected)
            {
                this.LoadCustomers(res_name.ToLower(), token);
                e.Handled = true;
            }
            if (Available.IsSelected)
            {
                this.LoadContents(res_name.ToLower(), token);
                e.Handled = true;
            }

            e.Handled = true;
        }

        private async void LoadCustomers(string res_name, string token)
        {
            //while (true)
            {
                HttpClient client = new HttpClient();
                string uri = $"http://localhost:5000/restrv1/{res_name}/{token}/customers";
                HttpResponseMessage response = await client.GetAsync(uri);
                response.EnsureSuccessStatusCode();
                string responseString = await response.Content.ReadAsStringAsync();
                List<Booking> bookings = JsonConvert.DeserializeObject<List<Booking>>(responseString);
                lvBookings.ItemsSource = bookings;

            }
        }
        private async void Remove_Click(object sender, RoutedEventArgs e)
        {
            var selectedSlot = lvSlots.SelectedItems[0] as TimeSlot;
            HttpClient client = new HttpClient();
            string uri = $"http://localhost:5000/restrv1/{res_name}/{token}/delete";
            var request = new HttpRequestMessage(HttpMethod.Delete, uri);
            request.Content = new StringContent(JsonConvert.SerializeObject(selectedSlot), Encoding.UTF8, "application/json");
            HttpResponseMessage response = client.SendAsync(request).Result;
            if (response.IsSuccessStatusCode)
            {
                this.LoadContents(res_name.ToLower(), token);
            }

        }

        private void addTime_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
            AddTimeForm addTime = new AddTimeForm(res_name,token);
            addTime.ShowDialog();
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            var selectedSlot = lvBookings.SelectedItems[0] as Booking;
            HttpClient client = new HttpClient();
            string uri = $"http://localhost:5000/restrv1/{res_name}/{token}/delete/booking";
            var request = new HttpRequestMessage(HttpMethod.Delete, uri);
            request.Content = new StringContent(JsonConvert.SerializeObject(selectedSlot), Encoding.UTF8, "application/json");
            HttpResponseMessage response = client.SendAsync(request).Result;
            if (response.IsSuccessStatusCode)
            {
                this.LoadCustomers(res_name.ToLower(), token);
            }
        }

        private void lvBookings_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            e.Handled = true;
        }

        private void lvSlots_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            e.Handled = true;
        }
    }
}
