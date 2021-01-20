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
using System.Windows.Shapes;

namespace ResUI
{
    /// <summary>
    /// Interaction logic for AddTimeForm.xaml
    /// </summary>
    public partial class AddTimeForm : Window
    {
        public string token { get; set; }

        public string res_name { get; set; }

        public AddTimeForm()
        {
            InitializeComponent();
        }

        public AddTimeForm(string rest_name, string Token)
        {
            InitializeComponent();
            token = Token;
            res_name = rest_name;
        }
        private void Close_Form(object sender, RoutedEventArgs e)
        {
            this.Close();
            MainWindow mainWindow = new MainWindow();
            mainWindow.ShowDialog();
        }

        private void AddTime_Click(object sender, RoutedEventArgs e)
        {
            TimeSlot timeSlot = new TimeSlot();
            timeSlot.timeslot = AvFrom.Text + "-" + AvEnd.Text;
            timeSlot.available = AvailableSeats.Text;
            HttpClient client = new HttpClient();
            string output = JsonConvert.SerializeObject(timeSlot);
            var httpContent = new StringContent(output, Encoding.UTF8, "application/json");
            HttpResponseMessage responseMessage = client.PutAsync($"http://localhost:5000/restrv1/{res_name}/{token}/addSlot", content: httpContent).Result;
            if (responseMessage.IsSuccessStatusCode)
            {
                this.Close();
                MainWindow mainWindow = new MainWindow(res_name,token);
                mainWindow.ShowDialog();
            }

        }
    }
}
