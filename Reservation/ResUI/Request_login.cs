using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResUI
{
    class Request_login
    {
        public string username { get; set; }

        public string cnonce { get; set; }

        public string hash { get; set; }
    }
}
