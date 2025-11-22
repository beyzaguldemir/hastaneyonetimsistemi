import { useEffect, useState } from 'react';
import { departmentsAPI, doctorsAPI, patientsAPI, appointmentsAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    departments: 0,
    doctors: 0,
    patients: 0,
    appointments: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [deptsRes, doctorsRes, patientsRes, appsRes] = await Promise.all([
          departmentsAPI.getAll(),
          doctorsAPI.getAll(),
          patientsAPI.getAll(),
          appointmentsAPI.getAll(),
        ]);

        setStats({
          departments: deptsRes.data.length,
          doctors: doctorsRes.data.length,
          patients: patientsRes.data.length,
          appointments: appsRes.data.length,
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const statCards = [
    { label: 'Departmanlar', value: stats.departments, icon: '🏥', color: 'bg-blue-500' },
    { label: 'Doktorlar', value: stats.doctors, icon: '👨‍⚕️', color: 'bg-green-500' },
    { label: 'Hastalar', value: stats.patients, icon: '👥', color: 'bg-purple-500' },
    { label: 'Randevular', value: stats.appointments, icon: '📅', color: 'bg-orange-500' },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Yükleniyor...</div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div
            key={index}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">{stat.label}</p>
                <p className="text-3xl font-bold text-gray-800 mt-2">{stat.value}</p>
              </div>
              <div className={`${stat.color} text-white p-4 rounded-full text-3xl`}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Hoş geldiniz! 👋</h2>
        <p className="text-gray-600">
          Hastane Yönetim Sistemine hoş geldiniz. Sol menüden departmanlar, doktorlar, 
          hastalar ve randevular bölümlerine erişebilirsiniz.
        </p>
      </div>
    </div>
  );
};

export default Dashboard;




