-- FixMyRoad Database Schema
-- PostgreSQL schema for Supabase

-- Create pothole_reports table
CREATE TABLE IF NOT EXISTS pothole_reports (
    id BIGSERIAL PRIMARY KEY,
    ticket_id VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) NOT NULL DEFAULT 'low',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    description TEXT,
    severity VARCHAR(20),
    image_url TEXT,
    reporter_name VARCHAR(100),
    reporter_email VARCHAR(100),
    reporter_phone VARCHAR(20),
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_pothole_reports_ticket_id ON pothole_reports(ticket_id);
CREATE INDEX IF NOT EXISTS idx_pothole_reports_status ON pothole_reports(status);
CREATE INDEX IF NOT EXISTS idx_pothole_reports_priority ON pothole_reports(priority);
CREATE INDEX IF NOT EXISTS idx_pothole_reports_location ON pothole_reports(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_pothole_reports_created_at ON pothole_reports(created_at);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_pothole_reports_updated_at ON pothole_reports;
CREATE TRIGGER update_pothole_reports_updated_at
    BEFORE UPDATE ON pothole_reports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE pothole_reports IS 'Stores pothole reports submitted by users';
COMMENT ON COLUMN pothole_reports.ticket_id IS 'Unique ticket identifier (format: FMR-YYYYMMDD-XXXXX)';
COMMENT ON COLUMN pothole_reports.status IS 'Current status: pending, in_progress, resolved, rejected';
COMMENT ON COLUMN pothole_reports.priority IS 'Priority based on area complaint density: low, medium, high, critical';
COMMENT ON COLUMN pothole_reports.latitude IS 'Latitude coordinate of pothole location';
COMMENT ON COLUMN pothole_reports.longitude IS 'Longitude coordinate of pothole location';
COMMENT ON COLUMN pothole_reports.severity IS 'User-reported severity level';
COMMENT ON COLUMN pothole_reports.image_url IS 'URL to uploaded pothole image';
COMMENT ON COLUMN pothole_reports.admin_notes IS 'Administrative notes and updates';
