import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // In a real app, this would fetch data from your backend API
    // For now, we'll return mock data that matches the expected structure
    const mockData = {
      patient_metrics: {
        total_patients: 1248,
        active_patients: 876,
        inactive_patients: 372,
        average_engagement: 67.5
      },
      campaign_metrics: {
        active_campaigns: 4,
        total_sent: 12450,
        delivered_rate: 98.2,
        response_rate: 63.5
      },
      recent_campaigns: [
        {
          id: 1,
          title: "Diabetes Follow-up Q2",
          is_active: true,
          start_date: "2025-04-01T00:00:00Z",
          end_date: "2025-06-30T00:00:00Z",
          response_rate: 72.4
        },
        {
          id: 2,
          title: "Hypertension Awareness",
          is_active: true,
          start_date: "2025-03-15T00:00:00Z",
          end_date: "2025-05-15T00:00:00Z",
          response_rate: 58.9
        },
        {
          id: 3,
          title: "Annual Check-up Reminder",
          is_active: false,
          start_date: "2025-01-01T00:00:00Z",
          end_date: "2025-03-31T00:00:00Z",
          response_rate: 82.1
        },
        {
          id: 4,
          title: "COVID Booster Information",
          is_active: true,
          start_date: "2025-04-20T00:00:00Z",
          end_date: "2025-07-20T00:00:00Z",
          response_rate: 45.7
        }
      ]
    };

    return NextResponse.json(mockData);
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch dashboard data' },
      { status: 500 }
    );
  }
}
