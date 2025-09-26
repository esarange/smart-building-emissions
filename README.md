# Smart Building Lifecycle Emissions Calculator with Digital Twin Interface

A FastAPI-based backend application that calculates cradle-to-grave emissions for smart building components and provides a digital twin interface for real-time scenario simulation. This system enables architects, engineers, and sustainability professionals to model building emissions and explore reduction strategies.

## Architecture Overview

### Design Patterns Implemented

#### 1. **Strategy Pattern** - Component Emissions Calculations
- **Purpose**: Encapsulate different emission calculation algorithms for various component types
- **Implementation**: Each component type (`EnergyComponent`, `MaterialComponent`, `WaterComponent`) implements the same `calculate_emissions()` interface but with type-specific logic
- **Benefit**: Enables polymorphic behavior - the `Building` class can call `component.calculate_emissions()` without knowing the concrete type

#### 2. **Factory Pattern** - Component Creation
- **Purpose**: Centralize and simplify object creation logic
- **Implementation**: `ComponentFactory` creates appropriate component instances based on type, handling parameter validation and initialization
- **Benefit**: Decouples component creation from business logic, making it easy to add new component types

#### 3. **Singleton Pattern** - Database Client Management
- **Purpose**: Ensure single database connection instance across the application
- **Implementation**: `DatabaseHandler` singleton manages Supabase client initialization and provides global access
- **Benefit**: Efficient resource usage and consistent database connection management

### Layered Architecture

```
Models (Pydantic) ←→ Controllers (FastAPI Routes) ←→ Services (Business Logic) ←→ Repositories (Data Access) ←→ Database
```

## 📁 Project Structure

```
smart-building-emissions/
│
├── src/
│   ├── api/                           # FastAPI Route Controllers
│   │   └── routes/
│   │       ├── buildings.py           # Building management endpoints
│   │       ├── components.py          # Component CRUD operations
│   │       └── emission_factors.py    # Emission factor management
│   │
│   ├── components/                    # Strategy Pattern Implementations
│   │   ├── base.py                    # Abstract Component class
│   │   ├── energy.py                  # Energy system calculations
│   │   ├── material.py                # Material embodied carbon
│   │   └── water.py                   # Water system emissions
│   │
│   ├── core/                          # Business Domain Models
│   │   ├── models.py                  # Pydantic schemas (DTOs)
│   │   ├── building.py                # Digital Twin building model
│   │   ├── calculator.py              # Emissions calculation engine
│   │   └── factory.py                 # Factory Pattern implementation
│   │
│   ├── data/                          # Data Access Layer
│   │   ├── database.py                # Singleton Database Handler
│   │   └── repositories.py            # Repository Pattern implementations
│   │
│   └── services/                      # Business Logic Layer
│       ├── building_service.py        # Building operations
│       ├── component_service.py       # Component management
│       ├── emission_factor_service.py # Emission factor operations
│       └── emission_service.py        # Emission calculation operations
│
├── requirements.txt                   # Python dependencies
├── main.py                           # FastAPI application entry point
└── .env.example                      # Environment variables template
```

## 🚀 API Endpoints Usage

Visit http://localhost:8000/docs after starting the api to see endpoints
```

## 💡 Key Features

### Digital Twin Capabilities
- **Real-time Parameter Adjustment**: Modify building parameters and see immediate emission impacts
- **Lifecycle Analysis**: Cradle-to-grave emissions across all building systems

### Component Types Supported
1. **Energy Systems**: HVAC, lighting, electrical systems
2. **Materials**: Structural elements, finishes, enclosures
3. **Water Systems**: Consumption, treatment, recycling

### Data Management
- **Emission Factor Database**: Comprehensive library of verified emission factors
- **Component Library**: Reusable component definitions

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.9+
- Supabase account
- Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/smart-building-emissions.git
   cd smart-building-emissions
   ```

2. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python scripts/init_db.py
   ```

5. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### Database Schema
The application uses the following main tables:
- `buildings` - Digital twin instances
- `components` - Reusable component definitions  
- `emission_factors` - Emission factor library
- `components_by_building` - Many-to-many building-component relationships

## 📊 Example Workflow

1. **Define Emission Factors** → Create material and energy emission factors
2. **Create Components** → Define HVAC systems, materials, water systems
3. **Assemble Building** → Add components to building digital twin with quantities
4. **Run Simulations** → Calculate emissions with different parameters
6. **Export Results** → Generate reports for stakeholders

## 🎯 Use Cases

### For Architects and Engineers
- Compare material choices for carbon impact
- Optimize building systems for sustainability
- Generate emissions reports for certifications (LEED, BREEAM)

### For Sustainability Consultants
- Rapid scenario analysis for client presentations
- Lifecycle assessment reporting
- Carbon reduction strategy development

### For Building Owners
- Operational carbon forecasting
- Retrofit planning and impact assessment
- ESG reporting and compliance

## 🔮 Future Enhancements

- **Real-time IoT Integration**: Connect to building management systems
- **Advanced Visualization**: 3D building model integration
- **Machine Learning**: Predictive emissions modeling
- **Regulatory Compliance**: Automated compliance checking
- **Supply Chain Integration**: Real-time material carbon data

**Built with FastAPI, Supabase, and Python** - Empowering sustainable building design through digital twin technology.